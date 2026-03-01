"""Baseline MCP Server — stdio transport entry point.

Usage:
    python3 -m mcp_server.server

Claude Desktop config:
    {
        "mcpServers": {
            "baseline": {
                "command": "python3",
                "args": ["-m", "mcp_server.server"],
                "cwd": "/Users/adeal/src/baseline"
            }
        }
    }
"""

from mcp.server.fastmcp import FastMCP

from mcp_server.tools import register_tools

mcp = FastMCP(
    "Baseline",
    instructions=(
        "Baseline is a local-first health data vault. "
        "It provides access to blood biomarkers with NHANES percentile rankings, "
        "Garmin wearable data (VO2 max, HRV, Zone 2, RHR), "
        "longitudinal lab trends, and health coverage scoring. "
        "Use get_health_context_for_plan for comprehensive summaries."
    ),
)

register_tools(mcp)

if __name__ == "__main__":
    mcp.run()
