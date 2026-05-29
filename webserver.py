import uasyncio as asyncio
import ujson
import ure
import time
from music_player import start_music, stop_music, resume_music, next_music, check_auto_stop
import bpm_sensor

# Load HTML page
try:
    with open('/static/index.html', 'r') as f:
        INDEX = f.read()
except:
    try:
        with open('index.html', 'r') as f:
            INDEX = f.read()
    except:
        INDEX = "<h1>index.html not found</h1>"

bpm_before = 0
bpm_after = 0

def _parse_genre_from_request(line: bytes) -> str:
    try:
        s = line.decode()
        m = ure.search(r'/start_music\?genre=([A-Za-z0-9_-]+)', s)
        if m:
            return m.group(1)
    except:
        pass
    return "calm"

async def serve(reader, writer):
    try:
        req_line = await reader.readline()
        # Drain headers
        while True:
            line = await reader.readline()
            if not line or line == b"\r\n":
                break

        line = req_line or b""
        path = line.split()[1] if len(line.split()) > 1 else b"/"

        if path.startswith(b"/start_music"):
            genre = _parse_genre_from_request(req_line or b"")
            start_music(genre)
            writer.write(b"HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\nPlaying (shuffle): " + genre.encode())

        elif path == b"/stop_music":
            stop_music()
            writer.write(b"HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\nStopped")

        elif path == b"/resume_music":
            resume_music()
            writer.write(b"HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\nResumed current track")

        elif path == b"/next_music":
            next_music()
            writer.write(b"HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\nNext track")

        elif path == b"/start":
            global bpm_before
            bpm_before = bpm_sensor.read_bpm(10)  # 10s capture
            payload = ujson.dumps({"bpm": bpm_before})
            writer.write(b"HTTP/1.0 200 OK\r\nContent-Type: application/json\r\n\r\n")
            writer.write(payload)

        elif path == b"/after":
            global bpm_after
            bpm_after = bpm_sensor.read_bpm(10)
            payload = ujson.dumps({"bpm": bpm_after})
            writer.write(b"HTTP/1.0 200 OK\r\nContent-Type: application/json\r\n\r\n")
            writer.write(payload)

        elif path.startswith(b"/feedback"):
            writer.write(b"HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\nThanks!")

        else:
            writer.write(b"HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n")
            writer.write(INDEX)

        await writer.drain()
    except Exception as e:
        try:
            writer.write(b"HTTP/1.0 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\n")
            writer.write(("Error: %s" % e).encode())
        except:
            pass
    finally:
        try:
            await writer.aclose()
        except:
            pass

async def auto_stop_loop():
    while True:
        check_auto_stop()
        await asyncio.sleep_ms(500)

async def run_server():
    server = await asyncio.start_server(serve, "0.0.0.0", 80)
    print("Web server running...")
    asyncio.create_task(auto_stop_loop())
    while True:
        await asyncio.sleep(1)

