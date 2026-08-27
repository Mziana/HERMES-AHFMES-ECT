param(
    [Parameter(Mandatory=$true)]
    [string]$ResultsDir
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $ResultsDir)) {
    throw "Results directory not found: $ResultsDir"
}

$rows = @()
foreach ($file in Get-ChildItem -Path $ResultsDir -Filter "B*.json" | Sort-Object Name) {
    $data = Get-Content -Raw -Encoding UTF8 $file.FullName | ConvertFrom-Json
    $rows += [PSCustomObject]@{
        Case = $data.case
        HasError = [bool]($data.error)
        ResponseLength = if ($data.response) { $data.response.Length } else { 0 }
        ManualScore = ""
        CriticalFailure = ""
        Notes = ""
    }
}

$out = Join-Path $ResultsDir "scores.csv"
$rows | Export-Csv -NoTypeInformation -Encoding UTF8 $out

Write-Host "Scoring sheet created: $out"
Write-Host "Fill ManualScore / CriticalFailure / Notes after reviewing each response."
