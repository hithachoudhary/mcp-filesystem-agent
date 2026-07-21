import anyio
from agent.mcp_client import client

async def main():

    print(
        await client.read_file(
            "test.txt"
        )
    )

    print(
        await client.write_file(
            "mcp_check.txt",
            "MCP Integration Verified"
        )
    )

    print(
        await client.read_file(
            "mcp_check.txt"
        )
    )

anyio.run(main)