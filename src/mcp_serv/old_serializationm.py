"""
Takes USB serial data and translates it into an HTTP request
Sends request to MCP server and returns response as USB serial data
"""
import serial
import msgpack
import asyncio
from dataclasses import asdict
from .tools.tool_types import *

from .main import handle_request

# If error "no such file exists", run "ls /dev/cu.*" to find the correct port and replace it below
AIRLOCK = serial.Serial("/dev/cu.usbmodem39326093082", 9600, timeout=10)

def send_serial(data: ToolResultSuccess | ToolResultError) -> None:
    """
    Sends data to the USB serial port
    """
    out_json = {"type": "tool_result", "data": asdict(data)}
    AIRLOCK.write(msgpack.packb(out_json))

print("Server is running, listening for incoming data...")
while True:
    # Read data from USB serial
    inp = msgpack.unpackb(AIRLOCK.readline())
    if not inp:
        continue
    if inp["type"] != "tool_call":
        continue
    try:
        # Parse the incoming data as an HTTP request
        output = asyncio.run(handle_request(ToolRequest(**inp["data"])))
        send_serial(output)
    except Exception as e:
        continue # ignore invalid requests
    # Request must be a valid JSON-RPC request