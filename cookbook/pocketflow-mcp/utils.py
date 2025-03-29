from openai import OpenAI
import os
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def call_llm(messages):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"))
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7
    )
    
    return response.choices[0].message.content

def get_tools(server_script_path):
    """Get available tools from an MCP server.
    """
    async def _get_tools():
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path]
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools_response = await session.list_tools()
                return tools_response.tools
    
    return asyncio.run(_get_tools())

def call_tool(server_script_path, tool_name, arguments):
    """Call a tool on an MCP server.
    """
    async def _call_tool():
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path]
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                return result.content[0].text
    
    return asyncio.run(_call_tool())

if __name__ == "__main__":
    # Test the LLM call
    messages = [{"role": "user", "content": "In a few words, what's the meaning of life?"}]
    response = call_llm(messages)
    print(f"Prompt: {messages[0]['content']}")
    print(f"Response: {response}")

        # Find available tools
    print("=== Finding available tools ===")
    tools = get_tools("simple_server.py")
    
    # Print tool information nicely formatted
    for i, tool in enumerate(tools, 1):
        print(f"\nTool {i}: {tool.name}")
        print("=" * (len(tool.name) + 8))
        print(f"Description: {tool.description}")
        
        # Parameters section
        print("Parameters:")
        properties = tool.inputSchema.get('properties', {})
        required = tool.inputSchema.get('required', [])
        
        # No parameters case
        if not properties:
            print("  None")
        
        # Print each parameter with its details
        for param_name, param_info in properties.items():
            param_type = param_info.get('type', 'unknown')
            req_status = "(Required)" if param_name in required else "(Optional)"
            print(f"  • {param_name}: {param_type} {req_status}")
    
    # Call a tool
    print("\n=== Calling the add tool ===")
    a, b = 5, 3
    result = call_tool("simple_server.py", "add", {"a": a, "b": b})
    print(f"Result of {a} + {b} = {result}")
    
    # You can easily call with different parameters
    a, b = 10, 20
    result = call_tool("simple_server.py", "add", {"a": a, "b": b})
    print(f"Result of {a} + {b} = {result}")

