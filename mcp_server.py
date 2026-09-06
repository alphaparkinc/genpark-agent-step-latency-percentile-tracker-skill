"""
MCP Server for genpark-agent-step-latency-percentile-tracker-skill
Standard JSON-RPC 2.0 protocol over stdio.
"""

import sys
import json
from client import StepLatencyPercentileTrackerClient

client = StepLatencyPercentileTrackerClient()

def handle_request(req):
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "record_latency",
                        "description": "Record agent execution step latency.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "step_name": {"type": "string"},
                                "latency_ms": {"type": "number"}
                            },
                            "required": ["step_name", "latency_ms"]
                        }
                    },
                    {
                        "name": "get_percentiles",
                        "description": "Get P50, P90, P95, P99 metrics for a step.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "step_name": {"type": "string"}
                            },
                            "required": ["step_name"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "record_latency":
            client.record_latency(args.get("step_name", ""), args.get("latency_ms", 0.0))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": "OK"}]}}
        elif tool_name == "get_percentiles":
            res = client.get_step_percentiles(args.get("step_name", ""))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
