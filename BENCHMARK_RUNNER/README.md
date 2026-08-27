# Hermes Local Benchmark Runner

This directory defines the local baseline runner for Llama 3.2 3B through Ollama.

## Purpose

Run the same benchmark cases against the base model before and after adaptation, then preserve raw outputs for comparison.

## Requirements

- Windows PowerShell
- Ollama running locally
- `ollama` available on PATH
- a local Hermes model tag, defaulting to `llama3.2:3b`

## Run

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\BENCHMARK_RUNNER\run_benchmark.ps1
```

Optional model:

```powershell
powershell -ExecutionPolicy Bypass -File .\BENCHMARK_RUNNER\run_benchmark.ps1 -Model "llama3.2:3b"
```

Optional output directory:

```powershell
powershell -ExecutionPolicy Bypass -File .\BENCHMARK_RUNNER\run_benchmark.ps1 -OutputDir ".\BENCHMARK_RUNNER\results\baseline-001"
```

## Important

The runner does not claim that an answer is correct. It captures model output so it can be evaluated against the expected behavior in each case.

Human/automated scoring is a separate stage.

## Baseline Identity

Record the exact result of:

```powershell
ollama show llama3.2:3b
```

and the runtime/context configuration used for the run.
