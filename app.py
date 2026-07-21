import gradio as gr

from agent.orchestrator import process_query


async def chat(message, history):

    response = await process_query(message)

    trace = "\n".join(response["trace"])

    result = response["result"]

    return f"""
TOOL TRACE

{trace}

RESULT

{result}
"""


demo = gr.ChatInterface(
    fn=chat,
    title="MCP Filesystem Agent",
    description="Ask questions about files in the sandbox directory."
)

demo.launch()