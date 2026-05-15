import websocket
import json
import socket
from uav_telemetry import UAVTelemetry


class UAVWebSocket:
    WS_URL = "ws://localhost:8080/drone-telemetry"
    WS_HOST = "localhost"

    def __init__(self):
        self.ws = websocket.WebSocket()

    def connect(self) -> bool:
        try:
            print(f"[*] Connecting to {self.WS_URL}...")

            self.ws.connect(self.WS_URL)

            print("[+] TCP/WebSocket connection established")

            connect_frame = (
                "CONNECT\n"
                "accept-version:1.2\n"
                f"host:{self.WS_HOST}\n"
                "\n"
                "\x00"
            )

            self.ws.send(connect_frame)

            print("[>] STOMP CONNECT frame sent")

            self.wait_connection_response()
            return True

        except ConnectionRefusedError:
            print("[-] Connection refused")
            print("    Is the Spring Boot server running on port 8080?")

        except socket.gaierror:
            print("[-] Invalid hostname")
            print(f"    Could not resolve host: {self.WS_HOST}")

        except websocket.WebSocketTimeoutException:
            print("[-] Connection timed out")

        except websocket.WebSocketConnectionClosedException:
            print("[-] WebSocket connection closed unexpectedly")

        except OSError as e:
            print(f"[-] OS/network error: {e}")

        except Exception as e:
            print(f"[-] Unexpected error: {type(e).__name__}")
            print(f"    Details: {e}")


    def wait_connection_response(self) -> bool:
        try:
            response = self.ws.recv()

            print("[<] CONNECT RESPONSE:")
            print(response)

            if response.startswith("CONNECTED"):
                print("[+] STOMP connection successful")
                return True
            else:
                print("[-] Unexpected STOMP response")


        except websocket.WebSocketTimeoutException:
            print("[-] Timed out waiting for STOMP response")

        except Exception as e:
            print(f"[-] Failed to receive response: {e}")

    def send_message(self, telemetry: UAVTelemetry):
        try:
            body = json.dumps(telemetry.data)

            send_frame = (
                "SEND\n"
                "destination:/app/telemetry\n"
                "content-type:application/json\n"
                f"content-length:{len(body)}\n"
                "\n"
                f"{body}\x00"
            )

            self.ws.send(send_frame)

            print("[>] Sent telemetry:")
            print(f"    {body}")

        except TypeError as e:
            print("[-] Failed to serialize telemetry object")
            print(f"    Details: {e}")

        except websocket.WebSocketConnectionClosedException:
            print("[-] Cannot send message")
            print("    WebSocket connection is closed")

        except Exception as e:
            print(f"[-] Failed to send telemetry: {e}")

    def close(self):
        try:
            self.ws.close()
            print("[+] Connection closed")

        except Exception as e:
            print(f"[-] Error while closing connection: {e}")