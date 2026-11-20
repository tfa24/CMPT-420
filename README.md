# Offline Knowledge Distillation for Static Binary Analysis

## About

This repository contains the implementation of project "Offline Knowledge Distillation for Static Binary Analysis". Teacher models analyze binaries in IDA Pro through `ida-pro-mcp`, their reverse engineering trajectories are collected into a supervised dataset, and a local student model is fine-tuned for downstream inference.

## Installation

To set up the environment on a CUDA GPU, run:

```bash
git submodule update --init --recursive
git -C llama.cpp apply ../llama.cpp.diff
mamba env create -f environment.yml
mamba activate 420
cmake -B llama.cpp/build -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=YOUR_GPU_ARCH
cmake --build llama.cpp/build --config Release -j
```

Generating the crackme binaries requires MSVC with C++20 support on Windows.

## Training Set Generation

The training set is collected from IDA Pro sessions on a synthetic crackme suite. `crackme/compile_all.py` builds seven challenge families, each emitted at four difficulty levels: `easy`, `medium`, `hard`, and `extreme`. Every family contributes three training binaries and one validation binary per difficulty, along with per-split `answer.json` files.

`easy` binaries have no compile time obfuscation. `medium` introduces Cloakwork control-flow macros: `CW_IF` and `CW_ELSE` expand to opaque-predicate branches, while `CW_BRANCH` routes conditions through an obfuscated indirect-branch path. `hard` keeps those control-flow transforms and adds data hiding: `CW_STR` emits XTEA-encrypted strings that decrypt at runtime, and `CW_CONST` replaces literals with encrypted compile-time constants. `extreme` adds `CW_PROTECT` and `CW_PROTECT_VOID`, which wrap the protected region in Cloakwork's encrypted state-machine dispatcher. Each build also patches challenge-specific constants at compile time to diversify the binaries.

Compile the crackmes with:

```bash
cd crackme
python compile_all.py
```

If you want to use the local `GLM-4.7-Flash` teacher, download the GGUF first:

```bash
hf download ggml-org/GLM-4.7-Flash-GGUF GLM-4.7-Flash-UD-Q4_K_XL.gguf --local-dir ./model/glm-4.7-flash-gguf/
```

Then start it with:

```bash
./llama.cpp/build/bin/llama-server \
    --ctx-size 200000 \
    --batch-size 4096 \
    --ubatch-size 1024 \
    --parallel 1 \
    --flash-attn on \
    --cache-type-k q8_0 \
    --cache-type-v q8_0 \
    --model ./model/glm-4.7-flash-gguf/GLM-4.7-Flash-UD-Q4_K_XL.gguf \
    --temp 0.7 \
    --top-p 1.0 \
    --min-p 0.01 \
    --kv-unified \
    --alias glm-4.7-flash \
    --host 127.0.0.1 \
    --port 9432 \
    --jinja \
    --reasoning-format deepseek
```

Before each collection run:

1. Rename the binary to a random UUIDv4.
2. Load it in IDA Pro.
3. Rebase it to `0x0`.
4. Start the IDA-side plugin from `Edit -> Plugins -> MCP` or press `Ctrl-Alt-M`.

Once the IDA-side plugin is running, start the transport bridge with:

```bash
ida-pro-mcp --ida-rpc http://127.0.0.1:13337 --transport http://127.0.0.1:9433/mcp
```

With the teacher endpoint and `ida-pro-mcp` running, append a trajectory to `train.jsonl` with:

```bash
python inference.py --model-endpoint http://127.0.0.1:9432/v1 --model-name glm-4.7-flash --mcp-endpoint http://127.0.0.1:9433/mcp --output-jsonl ./train.jsonl
```

For the third-party teachers, run the same pipeline against an OpenAI-compatible endpoint. `GLM-4.7-Flash` remains available as a local teacher, but most dataset generation is carried out with `GLM-5` and `GLM-5-Turbo` through third-party OpenAI-compatible endpoints.

We provide the collected `train.jsonl` dataset, along with the compiled crackmes and their solutions. The released binaries are not byte-identical to the ones used during dataset generation, but the difference is only in compile-time randomization.

| Artifact          | Download                                                                                                                                                                                      |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Training Set      | [Link](https://archive.org/download/offline-knowledge-distillation-for-static-binary-analysis/Offline%20Knowledge%20Distillation%20for%20Static%20Binary%20Analysis.zip/Training%20Set.jsonl) |
| Compiled Crackmes | [Link](https://archive.org/download/offline-knowledge-distillation-for-static-binary-analysis/Offline%20Knowledge%20Distillation%20for%20Static%20Binary%20Analysis.zip/Crackme.zip)          |

## Fine-Tuned Model

The student model is `zai-org/GLM-4.6V-Flash`. We fine-tune it with QLoRA on the tool-calling reverse engineering trajectories in `train.jsonl`. Training is driven by [finetune.py](finetune.py), with the hyperparameters defined in [config.py](config.py).

Run fine-tuning with:

```bash
python finetune.py --data-file ./train.jsonl --output-dir ./result/ --model-dir ./model/
```

We provide the HuggingFace LoRA adapter, the training log, the merged `llama.cpp` GGUF, and both vanilla and fine-tuned student evaluation outputs.

| Artifact                        | Download                                                                                                                                                                                                             |
|---------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| LoRA Adapter                    | [Link](https://archive.org/download/offline-knowledge-distillation-for-static-binary-analysis/Offline%20Knowledge%20Distillation%20for%20Static%20Binary%20Analysis.zip/LoRA.zip)                                    |
| Training Log                    | [Link](https://archive.org/download/offline-knowledge-distillation-for-static-binary-analysis/Offline%20Knowledge%20Distillation%20for%20Static%20Binary%20Analysis.zip/Training%20Logs.json)                        |
| Merged GGUF                     | [Link](https://archive.org/download/offline-knowledge-distillation-for-static-binary-analysis/Offline%20Knowledge%20Distillation%20for%20Static%20Binary%20Analysis.zip/GLM-4.6V-Flash-Q4_K_M-lora-merged.gguf)      |
| Fine-Tuned Student Eval Answers | [Link](https://archive.org/download/offline-knowledge-distillation-for-static-binary-analysis/Offline%20Knowledge%20Distillation%20for%20Static%20Binary%20Analysis.zip/Fine-Tuned%20Student%20Eval%20Answers.jsonl) |
| Vanilla Student Eval Answers    | [Link](https://archive.org/download/offline-knowledge-distillation-for-static-binary-analysis/Offline%20Knowledge%20Distillation%20for%20Static%20Binary%20Analysis.zip/Vanilla%20Student%20Eval%20Answers.jsonl)    |

`LoRA Adapter` is the Hugging Face PEFT adapter archive used to rebuild the model locally. `Merged GGUF` is the ready-to-serve `llama.cpp` artifact.

The following tables summarize validation results for the vanilla student and the fine-tuned student across the seven crackme families and four difficulty levels. All results are obtained following pass@1 evaluation.

### Vanilla Student Eval

|   | Easy                                     | Medium                                   | Hard                    | Extreme                 |
|---|------------------------------------------|------------------------------------------|-------------------------|-------------------------|
| 1 | Solved                                   | Confused by obfuscation                  | Hallucination           | Confused by obfuscation |
| 2 | Shift flow missed, key partially correct | Shift flow missed, key partially correct | Hallucination           | Hallucination           |
| 3 | Wrong solution                           | Confused by obfuscation                  | Confused by obfuscation | Confused by obfuscation |
| 4 | Hallucination                            | Hallucination                            | Ended agentic turn early | Confused by obfuscation |
| 5 | Hallucination                            | Confused by obfuscation                  | Confused by obfuscation | Confused by obfuscation |
| 6 | Hallucination                            | Solved                                   | Confused by obfuscation | Confused by obfuscation |
| 7 | Hallucination                            | Hallucination                            | Confused by obfuscation | Ended agentic turn early |

The vanilla student solved 2 out of 28 binaries, partially solved 2 binaries.

### Fine-Tuned Student Eval

|   | Easy                                     | Medium                                   | Hard                    | Extreme                 |
|---|------------------------------------------|------------------------------------------|-------------------------|-------------------------|
| 1 | Solved                                   | Solved                                   | Confused by obfuscation | Confused by obfuscation |
| 2 | Shift flow missed, key partially correct | Shift flow missed, key partially correct | Ended agentic turn early | Hallucination           |
| 3 | Hallucination                            | Hallucination                            | Confused by obfuscation | Confused by obfuscation |
| 4 | Solved                                   | Solved                                   | Confused by obfuscation | Confused by obfuscation |
| 5 | Constraint solved, example wrong         | Constraint solved, example wrong         | Confused by obfuscation | Confused by obfuscation |
| 6 | Solved                                   | Solved                                   | Confused by obfuscation | Confused by obfuscation |
| 7 | Key correct, wrong time constraint       | Key correct, wrong time constraint       | Confused by obfuscation | Confused by obfuscation |

The fine-tuned student solved 6 out of 28 binaries, partially solved 6 binaries. In family 5, the fine-tuned student correctly identified the key constraint, it failed to provide a correct example that satisfies the constraint, we consider this a partial solution.

## Inference

For local evaluation, you can either download the merged GGUF from us directly and skip the conversion steps, or rebuild it locally from the released LoRA adapter. If you want to build it yourself, download the base GGUF first:

```bash
hf download ggml-org/GLM-4.6V-Flash-GGUF GLM-4.6V-Flash-Q4_K_M.gguf --local-dir ./model/
```

Then convert the LoRA adapter to GGUF, merge it into the base model, and quantize the merged result back to `Q4_K_M`:

```bash
python llama.cpp/convert_lora_to_gguf.py --base-model-id zai-org/GLM-4.6V-Flash --outfile ./model/glm46v-flash-sft-lora-f16.gguf --outtype f16 ./result
./llama.cpp/build/bin/llama-export-lora -m ./model/GLM-4.6V-Flash-Q4_K_M.gguf -o ./model/GLM-4.6V-Flash-Q4_K_M-lora-merged-f16.gguf --lora ./model/glm46v-flash-sft-lora-f16.gguf
./llama.cpp/build/bin/llama-quantize ./model/GLM-4.6V-Flash-Q4_K_M-lora-merged-f16.gguf ./model/GLM-4.6V-Flash-Q4_K_M-lora-merged.gguf Q4_K_M
```

Serve the merged model with:

```bash
./llama.cpp/build/bin/llama-server \
    --ctx-size 131072 \
    --batch-size 4096 \
    --ubatch-size 1024 \
    --parallel 1 \
    --flash-attn on \
    --cache-type-k q8_0 \
    --cache-type-v q8_0 \
    --model ./model/GLM-4.6V-Flash-Q4_K_M-lora-merged.gguf \
    --temp 0.7 \
    --top-p 1.0 \
    --min-p 0.01 \
    --kv-unified \
    --alias glm-4.6v-flash \
    --host 127.0.0.1 \
    --port 9432 \
    --jinja \
    --reasoning-format deepseek \
    --no-mmproj
```

Once the model server and `ida-pro-mcp` are running, execute MCP-backed inference with:

```bash
python inference.py --model-endpoint http://127.0.0.1:9432/v1 --model-name glm-4.6v-flash --mcp-endpoint http://127.0.0.1:9433/mcp --output-jsonl ./output.jsonl
```
