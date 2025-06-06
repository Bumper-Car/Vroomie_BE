import os
import ssl
import asyncio
import websockets

from typing import Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/drive", tags=["drive"])

# 전역 WebSocketClientProtocol 객체 선언
colab_ws = None
connected_clients: Set[WebSocket] = set()

async def connect_to_colab_ws():
    global colab_ws
    url = os.getenv("COLAB_NGROK_URL") + "/"

    colab_ws = await websockets.connect(
        url,
        ssl=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2),
    )
    print("✅ Colab WebSocket 연결됨 (BE)")

async def broadcast_to_clients(message: str):
    for client in list(connected_clients):
        try:
            await client.send_text(message)
        except Exception as e:
            connected_clients.remove(client)
            print(f"❌ 클라이언트 전송 실패: {e}")

async def listen_from_colab():
    global colab_ws
    while True:
        try:
            if colab_ws is None:
                await connect_to_colab_ws()

            msg = await colab_ws.recv()
            print(f"📨 Colab에서 이벤트 수신: {msg}")
            await broadcast_to_clients(msg)

        except Exception as e:
            print(f"⚠️ Colab WebSocket 수신 중 오류: {e}")
            colab_ws = None
            await asyncio.sleep(1)

async def send_json_to_colab(json_text: str):
    global colab_ws
    try:
        if colab_ws is None:
            await connect_to_colab_ws()

        try:
            await colab_ws.send(json_text)
        except Exception as send_error:
            print(f"⚠️ WebSocket send 오류 발생 → 재연결 시도 ({send_error})")
            colab_ws = None
            await connect_to_colab_ws()
            asyncio.create_task(listen_from_colab())
            await colab_ws.send(json_text)

    except Exception as e:
        print(f"⚠️ Colab WebSocket 전체 오류 발생 ({e})")
        colab_ws = None

@router.websocket("/ws/video")
async def websocket_video(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    print("✅ WebSocket 연결됨")

    try:
        while True:
            json_text = await websocket.receive_text()
            await send_json_to_colab(json_text)

    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print("❌ WebSocket 연결 종료됨")
    except Exception as e:
        connected_clients.remove(websocket)
        print(f"⚠️ 예외 발생: {e}")
