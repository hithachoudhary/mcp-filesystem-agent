import anyio

from agent.mcp_client import client


async def main():

    result = await client.write_file(
        "hello_from_mcp.txt",
        "Hello from MCP Server"
    )

    print(result)

    content = await client.read_file(
        "hello_from_mcp.txt"
    )

    print(content)


anyio.run(main)