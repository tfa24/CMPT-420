import argparse
import asyncio
import json

import httpx
from openai import AsyncOpenAI
from pydantic_ai import (
    Agent,
    ModelRequest,
    ModelResponse,
    TextPart,
    ThinkingPart,
    ToolCallPart,
    ToolReturnPart,
    UsageLimits,
    UserPromptPart,
)
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

PROMPT = """You have been provided with a crackme binary loaded into the IDA Pro MCP. Your task is to reverse engineer the binary and extract the flag using static analysis only; running the binary or brute-forcing it is not allowed. You must produce a detailed report of your analysis, including the steps you took, the reasoning behind them, and the final flag. The flag may also be subject to additional constraints, so you must analyze the binary thoroughly to identify and understand those constraints.

Use the following systematic methodology:

1. **Decompilation Analysis**
   - Thoroughly inspect the decompiler output
   - Add detailed comments documenting your findings
   - Focus on understanding the actual functionality and purpose of each component

2. **Improve Readability in the Database**
   - Rename variables to sensible, descriptive names
   - Correct variable and argument types where necessary (especially pointers and array types)
   - Update function names to be descriptive of their actual purpose

3. **Deep Dive When Needed**
   - If more details are necessary, examine the disassembly and add comments with findings
   - Document any low-level behaviors that aren't clear from the decompilation alone
   - Explore using the callee tool and xref tool to understand the relationships between functions and data structures in the binary

4. **Important Constraints**
   - NEVER convert number bases yourself - use the int_convert MCP tool if needed
   - Use MCP tools to retrieve information as necessary
   - Derive all conclusions from actual analysis, not assumptions
   - Never run the binary, all information must be obtained through static analysis

5. **Documentation**
   - Document the steps taken and methodology used
   - Produce your report in chat that includes the flag and any constraints attached to it
"""


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--model-endpoint",
        type=str,
        default="http://127.0.0.1:9432/v1",
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default="glm-4.7-flash",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default="dummy",
    )
    parser.add_argument(
        "--mcp-endpoint",
        type=str,
        default="http://127.0.1:9433/mcp",
    )
    parser.add_argument(
        "--output-jsonl",
        type=str,
        default="./output.jsonl",
    )

    return parser.parse_args()


async def main():
    args = parse_args()

    server = MCPServerStreamableHTTP(args.mcp_endpoint)

    provider = OpenAIProvider(
        openai_client=AsyncOpenAI(
            base_url=args.model_endpoint,
            api_key=args.api_key,
            http_client=httpx.AsyncClient(timeout=None),
        )
    )

    agent = Agent(
        OpenAIChatModel(args.model_name, provider=provider), toolsets=[server]
    )

    usage_limits = UsageLimits(
        request_limit=None,
        tool_calls_limit=None,
        input_tokens_limit=None,
        output_tokens_limit=None,
        total_tokens_limit=None,
    )

    result = await agent.run(PROMPT, usage_limits=usage_limits)

    if args.output_jsonl is not None:
        row = {
            "messages": [],
            "tools": json.dumps(
                [
                    {
                        "type": "function",
                        "function": {
                            "name": t.name,
                            "description": t.description or "",
                            "parameters": t.inputSchema
                            or {"type": "object", "properties": {}},
                        },
                    }
                    for t in await server.list_tools()
                ],
                ensure_ascii=False,
            ),
        }

        for msg in result.new_messages():
            if isinstance(msg, ModelRequest):
                for part in msg.parts:
                    if isinstance(part, UserPromptPart):
                        row["messages"].append({"role": "user", "content": part.content})
                    elif isinstance(part, ToolReturnPart):
                        row["messages"].append(
                            {
                                "role": "tool",
                                "name": part.tool_name,
                                "content": part.model_response_str(),
                            }
                        )
            elif isinstance(msg, ModelResponse):
                reasoning = "\n".join(
                    part.content for part in msg.parts if isinstance(part, ThinkingPart)
                )
                content = "".join(
                    part.content for part in msg.parts if isinstance(part, TextPart)
                )
                tool_calls = [
                    {
                        "type": "function",
                        "function": {
                            "name": part.tool_name,
                            "arguments": part.args_as_dict(),
                        },
                    }
                    for part in msg.parts
                    if isinstance(part, ToolCallPart)
                ]

                assistant = {"role": "assistant"}
                if reasoning:
                    assistant["reasoning_content"] = reasoning
                if tool_calls:
                    assistant["tool_calls"] = tool_calls
                if content:
                    assistant["content"] = content
                if len(assistant) > 1:
                    row["messages"].append(assistant)

        with open(args.output_jsonl, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(result.output)


asyncio.run(main())
