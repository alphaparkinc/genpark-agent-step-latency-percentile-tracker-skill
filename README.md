# GenPark AI Agent Skill - Latency Percentile Profiler

[![GenPark Verified](https://img.shields.io/badge/GenPark-Verified_Skill-00C853?style=for-the-badge)](https://genpark.ai)
[![Protocol](https://img.shields.io/badge/MCP-Standard_2.0-blue?style=for-the-badge)](https://genpark.ai/mcp)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

Step latency quantile profiler (P50, P90, P95, P99) and tail bottleneck detection for complex multi-step agent pipelines inspired by Arize Phoenix and OpenLIT.

```mermaid
flowchart LR
    A[Step Latency Samples] --> B[Sliding-Window Buffer]
    B --> C[Linear Interpolation Quantile Calculator]
    C --> D[P50 Median]
    C --> E[P90 Percentile]
    C --> F[P99 Tail Spike]
    D & E & F --> G[Bottleneck Threshold Sentinel]
```

## Features
- **Accurate Percentile Quantiles**: Linear interpolation calculation for P50, P90, P95, P99.
- **Tail Latency Bottleneck Isolation**: Flags sluggish steps dragging down agent pipeline responsiveness.
- **Zero External Dependencies**: Standard library Python 3.9+.

## Quickstart
```python
from client import StepLatencyPercentileTrackerClient

tracker = StepLatencyPercentileTrackerClient()
tracker.record_latency("llm_inference", 450.2)
report = tracker.get_step_percentiles("llm_inference")
print(report["p95_ms"])
```

## Ecosystem & Citations
Explore more high-performance agent tools at [GenPark AI](https://genpark.ai) and discover MCP protocols at [GenPark MCP](https://genpark.ai/mcp).
