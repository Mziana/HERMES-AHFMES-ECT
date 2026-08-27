param(
    [string]$Model = "llama3.2:3b",
    [string]$CasesDir = "$PSScriptRoot\..\EVALUATION\CASES_V02",
    [string]$OutputDir = "$PSScriptRoot\results\blind-v0.2-$(Get-Date -Format yyyyMMdd-HHmmss)",
    [int]$NumCtx = 65536,
    [string]$CaseFilter = "B*.md",
    [double]$Temperature = 0,
    [switch]$StopOnError
)
$ErrorActionPreference = "Stop"
function Require-Command([string]$Name) { if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) { throw "Required command not found: $Name" } }
function Read-Utf8File([string]$Path) { return [System.IO.File]::ReadAllText($Path, [System.Text.Encoding]::UTF8) }
function Write-Utf8File([string]$Path, [string]$Content) { [System.IO.File]::WriteAllText($Path, $Content, (New-Object System.Text.UTF8Encoding($false))) }
function Invoke-OllamaGenerate([string]$JsonBody) {
    $tempRequest = Join-Path $env:TEMP ("hermes-ollama-v02-" + [guid]::NewGuid().ToString("N") + ".json")
    try {
        Write-Utf8File $tempRequest $JsonBody
        $raw = & curl.exe --silent --show-error --write-out "`n__HERMES_HTTP_STATUS__:%{http_code}" --header "Content-Type: application/json; charset=utf-8" --data-binary "@$tempRequest" "http://localhost:11434/api/generate" 2>&1
        if ($LASTEXITCODE -ne 0) { throw "curl.exe failed with exit code $LASTEXITCODE. Output: $($raw -join "`n")" }
        $joined = $raw -join "`n"; $marker = "`n__HERMES_HTTP_STATUS__:"; $idx = $joined.LastIndexOf($marker)
        if ($idx -lt 0) { throw "Could not parse HTTP status from curl output." }
        [PSCustomObject]@{ StatusCode=[int]$joined.Substring($idx+$marker.Length).Trim(); Body=$joined.Substring(0,$idx) }
    } finally { Remove-Item -LiteralPath $tempRequest -Force -ErrorAction SilentlyContinue }
}
Require-Command "ollama"; Require-Command "curl.exe"
if (-not (Test-Path $CasesDir)) { throw "Cases directory not found: $CasesDir" }
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$metadata = [ordered]@{ evaluation="blind-v0.2"; timestamp=(Get-Date).ToString("o"); model=$Model; num_ctx_requested=$NumCtx; temperature=$Temperature; case_filter=$CaseFilter; powershell=$PSVersionTable.PSVersion.ToString(); input_encoding="UTF-8 explicit"; output_encoding="UTF-8 without BOM"; ollama_version=(& ollama --version | Out-String).Trim(); ground_truth_exposure="none" }
Write-Utf8File "$OutputDir\run_metadata.json" ($metadata | ConvertTo-Json -Depth 10)
$cases = Get-ChildItem -Path $CasesDir -Filter $CaseFilter | Sort-Object Name
if (-not $cases -or @($cases).Count -eq 0) { throw "No blind benchmark cases matched: $CaseFilter" }
foreach ($case in @($cases)) {
    $caseText = Read-Utf8File $case.FullName
    $prompt = @"
You are Hermes, an external cognitive tandem for AHFMES.

Operate as a rigorous software architect and engineering consultant.

Core operating rules:
- Separate observed evidence, user-supplied context, inference, and assumption.
- Never fabricate tool use, repository inspection, sources, or verification.
- If evidence is insufficient, identify what is unknown and what evidence would resolve it.
- Challenge flawed premises when technically justified.
- Distinguish recommendation from authority or current system state.
- Treat implementation as unverified until appropriate verification exists.
- Respect scope, safety, reversibility, and explicit authorization.
- Prefer concrete next actions over vague advice.

The following is the complete model-visible benchmark case. Do not assume that you have performed any action not represented here.

$caseText

Respond with the best engineering answer you can derive from the case. Do not mention hidden evaluation criteria.
"@
    $requestObject=[ordered]@{ model=$Model; prompt=$prompt; stream=$false; options=[ordered]@{num_ctx=$NumCtx; temperature=$Temperature} }
    $json=$requestObject | ConvertTo-Json -Depth 12 -Compress; $safeName=[IO.Path]::GetFileNameWithoutExtension($case.Name); $outFile=Join-Path $OutputDir "$safeName.json"
    try {
        $result=Invoke-OllamaGenerate $json
        if ($result.StatusCode -ge 200 -and $result.StatusCode -lt 300) {
            $ollama=$result.Body | ConvertFrom-Json
            $record=[ordered]@{ evaluation="blind-v0.2"; case=$case.Name; model=$Model; num_ctx=$NumCtx; temperature=$Temperature; http_status=$result.StatusCode; prompt=$prompt; response=$ollama.response; done=$ollama.done; done_reason=$ollama.done_reason; total_duration=$ollama.total_duration; load_duration=$ollama.load_duration; prompt_eval_count=$ollama.prompt_eval_count; eval_count=$ollama.eval_count }
            Write-Utf8File $outFile ($record | ConvertTo-Json -Depth 12); Write-Host "OK  $($case.Name) [$($result.StatusCode)]"
        } else {
            $record=[ordered]@{evaluation="blind-v0.2";case=$case.Name;model=$Model;num_ctx=$NumCtx;http_status=$result.StatusCode;prompt=$prompt;ollama_error_body=$result.Body}; Write-Utf8File $outFile ($record | ConvertTo-Json -Depth 12); Write-Warning "FAIL $($case.Name) [$($result.StatusCode)]"; if ($StopOnError) { throw "Ollama returned HTTP $($result.StatusCode) for $($case.Name)" }
        }
    } catch {
        if (-not (Test-Path $outFile)) { Write-Utf8File $outFile (([ordered]@{evaluation="blind-v0.2";case=$case.Name;model=$Model;num_ctx=$NumCtx;runner_error=$_.Exception.Message}) | ConvertTo-Json -Depth 12) }
        Write-Warning "RUNNER ERROR $($case.Name): $($_.Exception.Message)"; if ($StopOnError) { throw }
    }
}
Write-Host "Blind benchmark complete. Raw results: $OutputDir"