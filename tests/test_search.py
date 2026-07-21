import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

import anyio
from agent.mcp_client import client


async def main():

    print("SEARCHING FOR CSV FILES...\n")

    result = await client.search_files(".csv")

    print(result)


anyio.run(main)