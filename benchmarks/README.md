# Benchmarks

This directory contains benchmarks used to evaluate **Haalo**. 

Each subfolder corresponds to a different benchmark and contains a `run_benchmark.py` script and a corresponding `report.json` with the benchmark results.

> [!NOTE]
> The benchmark input consists of 1,000 multi-category <a href="https://arxiv.org/">arXiv</a> documents from the <a href="https://huggingface.co/datasets/vectara/open_ragbench">Open RAG Benchmark</a>.

## Preprocessing

### Description

This benchmark measures the time required to process uploaded documents across
_Academic Document Validation_, _PDF to Markdown Conversion_, _Chunking_, and
_Embedding & Indexing_ steps.

To run this benchmark:
```sh
make benchmark-preprocessing
```

### Results

| Commit | Hardware | Results |
|---|---|---|
| [`0b6cfc4`](https://github.com/michelepatella/haalo/commit/0b6cfc4) | MacBook Air M2, 8 GB | [View report](https://github.com/michelepatella/haalo/blob/0b6cfc4/benchmarks/preprocessing/report.json) |
| [`c713e7b`](https://github.com/michelepatella/haalo/commit/c713e7b) | MacBook Air M2, 8 GB | [View report](https://github.com/michelepatella/haalo/blob/c713e7b/benchmarks/preprocessing/report.json) |
| [`b0d631f`](https://github.com/michelepatella/haalo/commit/b0d631f) | MacBook Air M2, 8 GB | [View report](https://github.com/michelepatella/haalo/blob/b0d631f/benchmarks/preprocessing/report.json) |
