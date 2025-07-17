import asyncio
from fastmcp import Client

async def main():
    async with Client("examples/twilio_whatsapp.py") as client:
        result = await client.call_tool("send_whatsapp", {
            "to_number": "+923187118450",  # Your actual number
            "message": "✅ WhatsApp message from FastMCP is working!"
        })
        # The result's data is inside result.data
        print("💬 WhatsApp Status:", result.data)

asyncio.run(main())
