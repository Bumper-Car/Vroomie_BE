import os
import ssl
import base64
import websockets
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/drive", tags=["drive"])

# 전역 WebSocketClientProtocol 객체 선언
colab_ws = None

async def connect_to_colab_ws():
    global colab_ws
    url = os.getenv("COLAB_NGROK_URL") + "/"

    colab_ws = await websockets.connect(
        url,
        ssl=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2),
    )
    print("✅ Colab WebSocket 연결됨 (BE)")

async def send_frame_to_colab_direct(image_bytes: bytes):
    global colab_ws
    try:
        if colab_ws is None:
            await connect_to_colab_ws()

        try:
            await colab_ws.send(image_bytes)
        except Exception as send_error:
            print(f"⚠️ WebSocket send 오류 발생 → 재연결 시도 ({send_error})")
            colab_ws = None
            await connect_to_colab_ws()
            await colab_ws.send(image_bytes)

    except Exception as e:
        print(f"⚠️ Colab WebSocket 전체 오류 발생 ({e})")
        colab_ws = None

@router.websocket("/ws/video")
async def websocket_video(websocket: WebSocket):
    await websocket.accept()
    print("✅ WebSocket 연결됨")

    try:
        while True:
            data = await websocket.receive_text()  # base64 문자열 수신
            img_data = base64.b64decode(data)
            await send_frame_to_colab_direct(img_data)

    except WebSocketDisconnect:
        print("❌ WebSocket 연결 종료됨")
    except Exception as e:
        print(f"⚠️ 예외 발생: {e}")
