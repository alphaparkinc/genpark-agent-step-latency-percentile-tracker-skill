"""
Demonstration of genpark-agent-step-latency-percentile-tracker-skill
"""

import random
from client import StepLatencyPercentileTrackerClient

def main():
    tracker = StepLatencyPercentileTrackerClient()

    # Simulate 100 agent runs with varying step latencies
    for _ in range(100):
        tracker.record_latency("prompt_formatting", random.uniform(5.0, 18.0))
        tracker.record_latency("embedding_retrieval", random.uniform(40.0, 120.0))
        # Long tail bottleneck
        llm_latency = random.uniform(300.0, 800.0) if random.random() > 0.1 else random.uniform(1200.0, 2500.0)
        tracker.record_latency("llm_generation", llm_latency)

    print("=== STEP PERCENTILE PROFILES ===")
    for step in ["prompt_formatting", "embedding_retrieval", "llm_generation"]:
        pct = tracker.get_step_percentiles(step)
        print(f"Step '{step}': P50={pct['p50_ms']}ms | P90={pct['p90_ms']}ms | P95={pct['p95_ms']}ms | P99={pct['p99_ms']}ms")

    print("\n=== DETECTED PIPELINE BOTTLENECKS ===")
    bottlenecks = tracker.get_codebase_bottlenecks(p95_threshold_ms=500.0)
    for b in bottlenecks:
        print(f"  [ALERT] {b['message']}")

if __name__ == "__main__":
    main()
