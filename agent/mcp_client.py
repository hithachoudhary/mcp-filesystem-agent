from mcp.client.session import ClientSession
from mcp.client.stdio import (
    stdio_client,
    StdioServerParameters,
)

SERVER_PARAMS = StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "sandbox",
    ],
)


class MCPFilesystemClient:

    async def _call_tool(self, tool_name, arguments):

        async with stdio_client(SERVER_PARAMS) as (
            read_stream,
            write_stream,
        ):
            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:

                await session.initialize()

                result = await session.call_tool(
                    tool_name,
                    arguments,
                )

                return result

    async def list_directory(self):

        result = await self._call_tool(
            "list_directory",
            {
                "path": "."
            }
        )

        return result.structuredContent["content"]

    async def read_file(self, filename):

        result = await self._call_tool(
            "read_text_file",
            {
                "path": filename
            }
        )

        return result.structuredContent["content"]

    async def write_file(
        self,
        filename,
        content,
    ):

        result = await self._call_tool(
            "write_file",
            {
                "path": filename,
                "content": content
            }
        )

        return result.structuredContent["content"]

    async def search_files(
        self,
        extension,
    ):

        result = await self._call_tool(
            "search_files",
            {
                "path": ".",
                "pattern": f"**/*{extension}"
            }
        )

        return result.structuredContent["content"]


client = MCPFilesystemClient()