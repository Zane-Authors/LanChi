import sys
import json
import httpx
import asyncio
import logging

# LanChi High-Performance Bridge: Stdio <-> HTTP (Port 5050)
# Optimized for speed and reliability.

SERVER_URL = "http://127.0.0.1:5050/mcp/rpc"

async def main():
    async with httpx.AsyncClient(timeout=120.0) as client:
        loop = asyncio.get_event_loop()
        sys.stderr.write("Bridge initialized. Waiting for IDE requests...\n")
        sys.stderr.flush()
        
        while True:
            line = await loop.run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue
            
            try:
                request = json.loads(line)
                method = request.get("method")
                request_id = request.get("id")
                
                # Debug log to IDE's stderr stream
                sys.stderr.write(f"Bridge >> Received: {method} (id={request_id})\n")
                sys.stderr.flush()

                # Forward to target server
                try:
                    response = await client.post(SERVER_URL, json=request)
                    
                    # Only return response if it was a Request (has ID)
                    if request_id is not None:
                        if response.status_code == 200:
                            resp_json = response.json()
                            sys.stdout.write(json.dumps(resp_json) + "\n")
                            sys.stdout.flush()
                            sys.stderr.write(f"Bridge << Sent Result (id={request_id})\n")
                        else:
                            error_resp = {
                                "jsonrpc": "2.0",
                                "id": request_id,
                                "error": {"code": -32000, "message": f"Server Status {response.status_code}"}
                            }
                            sys.stdout.write(json.dumps(error_resp) + "\n")
                            sys.stdout.flush()
                            sys.stderr.write(f"Bridge << Sent Error {response.status_code}\n")
                    else:
                        # Notification - no response needed
                        sys.stderr.write(f"Bridge << Notification forwarded\n")
                    
                except Exception as e:
                    if request_id is not None:
                        error_resp = {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {"code": -32603, "message": f"Bridge Connection Error: {str(e)}"}
                        }
                        sys.stdout.write(json.dumps(error_resp) + "\n")
                        sys.stdout.flush()
                    sys.stderr.write(f"Bridge Connection Error: {str(e)}\n")
                
                sys.stderr.flush()
                                    
            except json.JSONDecodeError:
                sys.stderr.write("Bridge Error: Invalid JSON input\n")
                sys.stderr.flush()
                continue
            except Exception as e:
                sys.stderr.write(f"Bridge Internal Error: {str(e)}\n")
                sys.stderr.flush()
                continue

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.stderr.write(f"Bridge Fatal Error: {str(e)}\n")
