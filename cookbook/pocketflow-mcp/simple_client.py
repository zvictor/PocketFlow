import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Set up connection to your server
    server_params = StdioServerParameters(
        command="python",
        args=["simple_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools
            tools_response  = await session.list_tools()
            
            # Extract tools information
            tools = tools_response.tools
            
            # Parse each tool
            for tool in tools:
                print("\nTool Information:")
                print(f"  Name: {tool.name}")
                print(f"  Description: {tool.description}")
                print(f"  Required Parameters: {tool.inputSchema.get('required', [])}")
                
                # Parse parameter information
                properties = tool.inputSchema.get('properties', {})
                print("  Parameters:")
                for param_name, param_info in properties.items():
                    param_type = param_info.get('type', 'unknown')
                    param_title = param_info.get('title', param_name)
                    print(f"    - {param_name} ({param_type}): {param_title}")
            
            # Call the add tool
            result = await session.call_tool("add", {"a": 5, "b": 3})
            result_value = result.content[0].text
            print(f"5 + 3 = {result_value}")

if __name__ == "__main__":
    asyncio.run(main())