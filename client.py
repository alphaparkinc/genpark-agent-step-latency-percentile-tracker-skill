"""
Sliding-Window Latency Percentile Tracker (P50, P90, P95, P99).
Zero external dependencies, standard library only.
"""

import math
from typing import Dict, List, Any, Optional

class StepLatencyPercentileTrackerClient:
    """
    Accumulates step latencies across agent execution phases,
    computes exact quantiles (P50, P90, P95, P99), and flags performance bottlenecks.
    """

    def __init__(self, max_samples_per_step: int = 1000):
        self.max_samples = max_samples_per_step
        # step_name -> list of latency in milliseconds
        self.step_latencies = {}

    def record_latency(self, step_name: str, latency_ms: float):
        """Records a step execution duration in ms."""
        if step_name not in self.step_latencies:
            self.step_latencies[step_name] = []
        
        self.step_latencies[step_name].append(latency_ms)
        if len(self.step_latencies[step_name]) > self.max_samples:
            self.step_latencies[step_name].pop(0)

    def _calculate_quantile(self, sorted_data: List[float], q: float) -> float:
        """Calculates exact percentile using linear interpolation."""
        if not sorted_data:
            return 0.0
        n = len(sorted_data)
        if n == 1:
            return sorted_data[0]
        pos = (n - 1) * q
        base = int(math.floor(pos))
        rest = pos - base
        if base + 1 < n:
            return sorted_data[base] + rest * (sorted_data[base + 1] - sorted_data[base])
        return sorted_data[base]

    def get_step_percentiles(self, step_name: str) -> Optional[Dict[str, Any]]:
        """Calculates P50, P90, P95, P99, min, max, avg for step."""
        samples = self.step_latencies.get(step_name, [])
        if not samples:
            return None

        sorted_samples = sorted(samples)
        p50 = self._calculate_quantile(sorted_samples, 0.50)
        p90 = self._calculate_quantile(sorted_samples, 0.90)
        p95 = self._calculate_quantile(sorted_samples, 0.95)
        p99 = self._calculate_quantile(sorted_samples, 0.99)
        avg = sum(samples) / len(samples)

        return {
            "step_name": step_name,
            "sample_count": len(samples),
            "min_ms": round(sorted_samples[0], 2),
            "avg_ms": round(avg, 2),
            "p50_ms": round(p50, 2),
            "p90_ms": round(p90, 2),
            "p95_ms": round(p95, 2),
            "p99_ms": round(p99, 2),
            "max_ms": round(sorted_samples[-1], 2)
        }

    def get_codebase_bottlenecks(self, p95_threshold_ms: float = 1000.0) -> List[Dict[str, Any]]:
        """Identifies agent pipeline steps exceeding target latency threshold."""
        bottlenecks = []
        for step in self.step_latencies:
            pct = self.get_step_percentiles(step)
            if pct and pct["p95_ms"] > p95_threshold_ms:
                bottlenecks.append({
                    "step_name": step,
                    "p95_ms": pct["p95_ms"],
                    "p99_ms": pct["p99_ms"],
                    "message": f"Step '{step}' exhibits high tail latency (P95: {pct['p95_ms']} ms > {p95_threshold_ms} ms)."
                })
        return sorted(bottlenecks, key=lambda b: b["p95_ms"], reverse=True)
