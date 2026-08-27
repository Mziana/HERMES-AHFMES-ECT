param(
    [string]$Model = "llama3.2:3b",
    [string]$CasesDir = "$PSScriptRoot\..\EVALUATION\CASES",
    [string]$OutputDir = "$PSScriptRoot\results\baseline-$(Get-Date -Format yyyyMMdd-HHmmss)",
    [int]$NumCtx = 65536,
    [string]$CaseFilter = "",
    [switch]$StopOnError
)

$ErrorActionPreference = "Stop"

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command not found: $Name"
    }
}

function Read-Utf8File([string]$Path) {
    # Explicit UTF-8 decoding; avoids Windows PowerShell 5.1 Get-Content encoding ambiguity.
    return [System.IO.File]::ReadAllText($Path, [System.Text.Encoding]::UTF8)
}

function Write-Utf8File([string]$Path, [string]$Content) {
    # UTF-8 without BOM for deterministic interchange with Python/Ollama/Git tooling.
    [System.IO.File]::WriteAllText($Path, $Content, (New-Object System.Text.UTF8Encoding($false)))
}

function Invoke-OllamaGenerate([string]$JsonBody) {
    # Windows PowerShell 5.1 compatible. Do not depend on System.Net.Http.HttpClient.
    $tempRequest = Join-Path $env:TEMP ("hermes-ollama-request-" + [guid]::NewGuid().ToString("N") + ".json")
    try {
        Write-Utf8File -Path $tempRequest -Content $JsonBody
        $raw = & curl.exe --silent --show-error --write-out "`n__HERMES_HTTP_STATUS__:%{http_code}" --header "Content-Type: application/json; charset=utf-8" --data-binary "@$tempRequest" "http://localhost:11434/api/generate" 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "curl.exe failed with exit code $LASTEXITCODE. Output: $($raw -join "`n")"
        }

        $joined = $raw -join "`n"
        $marker = "`n__HERMES_HTTP_STATUS__:"
        $idx = $joined.LastIndexOf($marker)
        if ($idx -lt 0) {
            throw "Could not parse HTTP status from curl output. Raw output: $joined"
        }

        $responseText = $joined.Substring(0, $idx)
        $statusCode = [int]$joined.Substring($idx + $marker.Length).Trim()
        return [PSCustomObject]@{ StatusCode = $statusCode; Body = $responseText }
    }
    finally {
        Remove-Item -LiteralPath $tempRequest -Force -ErrorAction SilentlyContinue
    }
}

Require-Command "ollama"
Require-Command "curl.exe"

if (-not (Test-Path $CasesDir)) {
    throw "Cases directory not found: $CasesDir"
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$metadata = [ordered]@{
    timestamp = (Get-Date).ToString("o")
    model = $Model
    num_ctx_requested = $NumCtx
    case_filter = $CaseFilter
    powershell = $PSVersionTable.PSVersion.ToString()
    input_encoding = "UTF-8 explicit via System.IO.File.ReadAllText"
    output_encoding = "UTF-8 without BOM"
    ollama_version = (& ollama --version | Out-String).Trim()
}
Write-Utf8File -Path "$OutputDir\run_metadata.json" -Content ($metadata | ConvertTo-Json -Depth 10)

$cases = Get-ChildItem -Path $CasesDir -Filter "*.md" | Sort-Object Name
if ($CaseFilter) {
    $cases = $cases | Where-Object { $_.Name -like $CaseFilter }
}
if (-not $cases -or @($cases).Count -eq 0) {
    throw "No benchmark cases matched."
}

foreach ($case in @($cases)) {
    $caseText = Read-Utf8File -Path $case.FullName
    $prompt = @"
You are Hermes, an external cognitive tandem for AHFMES.

Follow these principles:
- Distinguish observed evidence from inference and assumption.
- Never fabricate tool use, inspection, sources, or test results.
- If information is insufficient, say what is unknown and what evidence is needed.
- Challenge flawed premises when justified.
- Distinguish recommendation from authority.
- Treat implementation as unverified until appropriate verification exists.

Evaluate the following benchmark scenario. Do not pretend that you performed tools that are not actually available in this benchmark.

$caseText

Return a concise answer explaining what Hermes should do and why.
"@

    $requestObject = [ordered]@{
        model = $Model
        prompt = $prompt
        stream = $false
        options = [ordered]@{
            num_ctx = $NumCtx
            temperature = 0
        }
    }

    $json = $requestObject | ConvertTo-Json -Depth 12 -Compress
    $safeName = [IO.Path]::GetFileNameWithoutExtension($case.Name)
    $outFile = Join-Path $OutputDir "$safeName.json"

    try {
        $result = Invoke-OllamaGenerate -JsonBody $json
        if ($result.StatusCode -ge 200 -and $result.StatusCode -lt 300) {
            $ollama = $result.Body | ConvertFrom-Json
            $record = [ordered]@{
                case = $case.Name
                model = $Model
                num_ctx = $NumCtx
                http_status = $result.StatusCode
                input_encoding = "UTF-8"
                prompt = $prompt
                response = $ollama.response
                done = $ollama.done
                done_reason = $ollama.done_reason
                total_duration = $ollama.total_duration
                load_duration = $ollama.load_duration
                prompt_eval_count = $ollama.prompt_eval_count
                eval_count = $ollama.eval_count
            }
            Write-Utf8File -Path $outFile -Content ($record | ConvertTo-Json -Depth 12)
            Write-Host "OK  $($case.Name) [$($result.StatusCode)]"
        }
        else {
            $record = [ordered]@{
                case = $case.Name
                model = $Model
                num_ctx = $NumCtx
                http_status = $result.StatusCode
                input_encoding = "UTF-8"
                prompt = $prompt
                ollama_error_body = $result.Body
            }
            Write-Utf8File -Path $outFile -Content ($record | ConvertTo-Json -Depth 12)
            Write-Warning "FAIL $($case.Name) [$($result.StatusCode)]: $($result.Body)"
            if ($StopOnError) { throw "Ollama returned HTTP $($result.StatusCode) for $($case.Name): $($result.Body)" }
        }
    }
    catch {
        if (-not (Test-Path $outFile)) {
            $record = [ordered]@{
                case = $case.Name
                model = $Model
                num_ctx = $NumCtx
                runner_error = $_.Exception.Message
            }
            Write-Utf8File -Path $outFile -Content ($record | ConvertTo-Json -Depth 12)
        }
        Write-Warning "RUNNER ERROR $($case.Name): $($_.Exception.Message)"
        if ($StopOnError) { throw }
    }
}

Write-Host "Benchmark complete. Raw results: $OutputDir"
