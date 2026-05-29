import uasyncio as asyncio
import webserver

async def main():
    await webserver.run_server()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Server stopped manually")

