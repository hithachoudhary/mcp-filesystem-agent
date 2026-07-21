import json
from datetime import datetime

from agent.llm_client import ask_llm
from agent.mcp_client import client

pending_action = None

SYSTEM_PROMPT = """
You are a filesystem assistant.

You may ONLY operate on files inside the sandbox directory.

For general questions about your capabilities, only mention:

- list files
- read files
- create files
- edit files
- search files
- summarize files
- compare files

Do not claim support for functionality that is not implemented.

If the user asks who you are, what you are, or what you can do:

{
  "tool": "none",
  "response": "I am an MCP filesystem assistant. I can list files, read files, create files, edit files, search files, summarize files, and compare files inside the sandbox directory."
}

If the user asks a question unrelated to filesystem operations, files, directories, or your capabilities, return:

{
  "tool": "none",
  "response": "I am a filesystem assistant and can only help with files in the sandbox directory."
}

You are ONLY a filesystem assistant.

If a question is not related to:

- files
- directories
- file summaries
- file comparisons
- file creation
- file editing
- file searching

return:

{
  "tool":"none",
  "response":"I can only help with files inside the sandbox directory."
}

If user asks to summarize a file:

{
  "tool": "summarize_file",
  "filename": "report.txt"
}

If user asks to summarize all files:

{
  "tool": "summarize_all_files"
}

If user asks to compare files:

{
  "tool": "compare_files",
  "file1": "notes.txt",
  "file2": "report.txt"
}

If user asks to delete a file:

{
  "tool": "delete_not_supported"
}

If user asks for anything outside the sandbox:

{
  "tool": "deny"
}

Examples:

{
  "tool": "list_files"
}

{
  "tool": "read_file",
  "filename": "test.txt"
}

{
  "tool": "create_file",
  "filename": "hello.txt",
  "content": "Hello World"
}

{
  "tool": "edit_file",
  "filename": "hello.txt",
  "content": "Updated Content"
}

{
  "tool": "search_files",
  "extension": ".csv"
}

Return ONLY JSON.
No markdown.
No explanations.
"""


def log_tool_call(tool, args, result):
    with open("logs/tool_calls.log", "a") as f:
        f.write(
            f"\n[{datetime.now()}]\n"
            f"Tool: {tool}\n"
            f"Args: {args}\n"
            f"Result: {result}\n"
        )


async def process_query(query):

    global pending_action

    # overwrite confirmation
    if query.strip().upper() == "YES" and pending_action:

        filename = pending_action["filename"]
        content = pending_action["content"]

        result = await client.write_file(
            filename,
            content
        )

        pending_action = None

        return {
            "trace": [
                f"MCP: write_file('{filename}')"
            ],
            "result": result
        }

    prompt = f"""
{SYSTEM_PROMPT}

User Request:
{query}
"""

    model_response = ask_llm(prompt)

    try:
        decision = json.loads(model_response)

        tool = decision.get("tool")

        if tool:
            args = decision
        else:
            tool = decision.get("name")
            args = decision.get("arguments", {})

        if not tool:
            return {
                "trace": [],
                "result": (
                    f"Model returned invalid response:\n"
                    f"{model_response}"
                )
            }

        trace = []

        if tool == "deny":
            return {
                "trace": [],
                "result": (
                    "Access denied: "
                    "outside sandbox directory"
                )
            }

        if tool == "delete_not_supported":
            return {
                "trace": [],
                "result": (
                    "File deletion is not implemented."
                )
            }

        if tool == "none":
            return {
                "trace": [],
                "result": decision.get(
                    "response",
                    "I am an MCP filesystem assistant."
                )
            }

        if tool == "list_files":

            result = await client.list_directory()

            trace.append(
                "MCP: list_directory()"
            )

            log_tool_call(tool, args, result)

            return {
                "trace": trace,
                "result": result
            }

        if tool == "read_file":

            filename = args["filename"]

            result = await client.read_file(
                filename
            )

            trace.append(
                f"MCP: read_text_file('{filename}')"
            )

            log_tool_call(tool, args, result)

            return {
                "trace": trace,
                "result": result
            }

        if tool == "create_file":

            filename = args["filename"]
            content = args["content"]

            result = await client.write_file(
                filename,
                content
            )

            trace.append(
                f"MCP: write_file('{filename}')"
            )

            log_tool_call(tool, args, result)

            return {
                "trace": trace,
                "result": result
            }

        if tool == "edit_file":

            filename = args["filename"]
            content = args["content"]

            pending_action = {
                "filename": filename,
                "content": content
            }

            return {
                "trace": [],
                "result": (
                    f"This will overwrite "
                    f"{filename}. "
                    "Reply YES to continue."
                )
            }

        if tool == "search_files":

            extension = args["extension"]

            result = await client.search_files(
                extension
            )

            cleaned = result.replace(
                "/home/hitha/Documents/filesystem_agent/sandbox/",
                ""
            )

            trace.append(
                f"MCP: search_files('{extension}')"
            )

            log_tool_call(tool, args, cleaned)

            return {
                "trace": trace,
                "result": cleaned
            }

        if tool == "summarize_file":

            filename = args["filename"]

            content = await client.read_file(
                filename
            )

            summary = ask_llm(
                f"""
Summarize the following file:

{content}
"""
            )

            trace.append(
                f"MCP: read_text_file('{filename}')"
            )

            trace.append(
                "summarize_content()"
            )

            log_tool_call(
                tool,
                args,
                "summary_generated"
            )

            return {
                "trace": trace,
                "result": summary
            }

        if tool == "summarize_all_files":

            directory_text = (
                await client.list_directory()
            )

            files = []

            for line in directory_text.splitlines():

                if "[FILE]" in line:

                    filename = (
                        line.replace(
                            "[FILE]",
                            ""
                        )
                        .strip()
                    )

                    if filename.endswith(".txt"):
                        files.append(filename)

            combined_content = ""

            for file in files:

                content = await client.read_file(
                    file
                )

                trace.append(
                    f"MCP: read_text_file('{file}')"
                )

                combined_content += (
                    f"\n\nFILE: {file}\n\n{content}"
                )

            summary = ask_llm(
                f"""
Summarize all these files.

{combined_content}

Provide:
1. Overall summary
2. Key themes
3. Important action items
4. Risks or open issues
"""
            )

            trace.append(
                "summarize_all_files()"
            )

            log_tool_call(
                tool,
                {"files": files},
                "summary_generated"
            )

            return {
                "trace": trace,
                "result": summary
            }

        if tool == "compare_files":

            file1 = args["file1"]
            file2 = args["file2"]

            content1 = await client.read_file(
                file1
            )

            content2 = await client.read_file(
                file2
            )

            comparison = ask_llm(
                f"""
Compare these two files.

FILE 1 ({file1}):

{content1}

FILE 2 ({file2}):

{content2}

Provide:
- Similarities
- Differences
- Important observations
"""
            )

            trace.append(
                f"MCP: read_text_file('{file1}')"
            )

            trace.append(
                f"MCP: read_text_file('{file2}')"
            )

            trace.append(
                "compare_files()"
            )

            log_tool_call(
                tool,
                args,
                "comparison_generated"
            )

            return {
                "trace": trace,
                "result": comparison
            }

        return {
            "trace": [],
            "result": f"Unknown tool: {tool}"
        }

    except Exception as e:
        return {
            "trace": [],
            "result": f"Error: {e}"
        }