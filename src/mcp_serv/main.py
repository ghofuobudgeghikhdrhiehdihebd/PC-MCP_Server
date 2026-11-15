"""
Takes USB serial data and translates it into an HTTP request
Sends request to MCP server and returns response as USB serial data
"""
import serial
import msgpack
from pjrpc import Request, Response
from .server import app

# If no data is ever received, check if these ports still work. Could change for no reason.
AIRLOCK_IN = serial.Serial("/dev/tty.usbmodem39326093082", 9600, timeout=10)
AIRLOCK_OUT = serial.Serial("/dev/cu.usbmodem39326093082", 9600, timeout=10)

def send_serial(data: Response) -> None:
    """
    Sends data to the USB serial port
    """
    AIRLOCK_OUT.write(msgpack.packb(data))


while True:
    # Read data from USB serial
    inp = msgpack.unpackb(AIRLOCK_IN.readline())
    if not inp:
        continue
    try:
        request = Request.from_json(inp)
        output = app.post("/", json=request.to_json())
        send_serial(Response.from_json(output.json()))
    except Exception as e:
        continue # ignore invalid requests
    # Request must be a valid JSON-RPC request