# Benchmarks

This directory contains benchmarks used to evaluate **Haalo**. 

Each subfolder corresponds to a different benchmark and contains a `run_benchmark.py` script and a corresponding `report.json` with the benchmark results.

> [!NOTE]
> All evaluations are performed on 1,000 multi-category <a href="https://arxiv.org/">arXiv</a> documents from the <a href="https://huggingface.co/datasets/vectara/open_ragbench">Open RAG Benchmark</a>.

## Preprocessing

### Description

This benchmark measures the time required to process uploaded documents across _PDF to Markdown Conversion_, _Chunking_, and _Embedding & Indexing_ steps.

To run this benchmark:
```sh
make benchmark-preprocessing
```

### Results

| Commit | Hardware | Avg. PDF to Markdown Conversion Time (s) | Avg. Chunking Time (s) | Avg. Embedding & Indexing Time (s) | Avg. Total Time (s) |
|---|---:|---:|---:|---:|---:|
| [`0b6cfc4`](https://github.com/michelepatella/haalo/commit/0b6cfc4789eb38cc07b34e5fbf290f2adb2a7b3b) | MacBook Air M2, 8 GB | 8.27 | 0.06 | 6.53 | **14.86** |
| [`c713e7b`](https://github.com/michelepatella/haalo/commit/c713e7b2f6c68bf07a4293317380c9d63dbfefcb) | MacBook Air M2, 8 GB | 9.48<br><sup>+14.7%</sup> | 0.06<br><sup>±0.0%</sup> | 1.12<br><sup>-82.9%</sup> | **10.66**<br><sup><strong>−28.3%</strong></sup> |

<sub>Percentages show the change from the previous commit.</sub>
