# Unified Regression Evaluation Gate Runner for HERMES-AHFMES-ECT

param(
    [string]$Model = "hermes-v0.2",
    [switch]$SkipV02,
    [switch]$SkipV03
)

$ErrorActionPreference = "Stop"
$ScriptDir = $PSScriptRoot

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  HERMES-AHFMES-ECT UNIFIED REGRESSION EVALUATION GATE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Dataset Validation
Write-Host "`n[STEP 1/3] Validating Dataset Integrity..." -ForegroundColor Yellow
python "$ScriptDir\..\TRAINING\validate_dataset.py" "$ScriptDir\..\TRAINING\DATASET_V0.2.jsonl"
python "$ScriptDir\..\TRAINING\validate_dataset.py" "$ScriptDir\..\TRAINING\DATASET_V0.3_SAMPLE.jsonl"

# 2. V0.2 Blind Benchmark Execution
if (-not $SkipV02) {
    Write-Host "`n[STEP 2/3] Running V0.2 Blind Benchmark Cases..." -ForegroundColor Yellow
    powershell -ExecutionPolicy Bypass -File "$ScriptDir\run_benchmark_v02.ps1" -Model $Model -CaseFilter "B*.md"
} else {
    Write-Host "`n[STEP 2/3] Skipped V0.2 Blind Benchmark (-SkipV02 flag set)" -ForegroundColor Gray
}

# 3. V0.3 Live-Tool Benchmark Execution
if (-not $SkipV03) {
    Write-Host "`n[STEP 3/3] Running V0.3 Live-Tool Benchmark Suite..." -ForegroundColor Yellow
    python "$ScriptDir\run_benchmark_v03.py"
} else {
    Write-Host "`n[STEP 3/3] Skipped V0.3 Live-Tool Benchmark (-SkipV03 flag set)" -ForegroundColor Gray
}

Write-Host "`n============================================================" -ForegroundColor Green
Write-Host "  EVALUATION GATE COMPLETE: System Ready for Audit Review" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
