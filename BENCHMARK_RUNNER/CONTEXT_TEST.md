# 64K Context Test

The model metadata may advertise a large context window, but the actual local runtime must be tested.

## Test objective

Determine whether the current Ollama setup can sustain a 64K-token request without unacceptable failure, truncation, memory exhaustion, or unusable latency.

## Important distinction

```text
model context metadata
        ≠
actual runtime capacity
        ≠
useful agent context
```

For Hermes, useful context should normally be assembled selectively. Loading an entire repository merely because the context window permits it is not the target architecture.

## Manual test

First inspect:

```powershell
ollama show llama3.2:3b
```

Then run a controlled generation request using the local Ollama API with `num_ctx` set to 65536. Measure:

- whether the request succeeds;
- peak VRAM;
- system RAM;
- latency;
- output completeness;
- whether Ollama reduces or rejects the requested context.

Record the exact result in the experiment journal.

## Warning

A GTX 1050 Ti with 4 GB VRAM may make a 64K runtime configuration impractical even if the model metadata supports it. Do not infer feasibility from metadata alone.
