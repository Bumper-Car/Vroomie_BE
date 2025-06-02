import os
import ssl

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
import base64
import websockets
import asyncio

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

async def listen_from_colab():
    global colab_ws
    while True:
        try:
            if colab_ws is None:
                await connect_to_colab_ws()

            msg = await colab_ws.recv()
            print(f"📨 Colab에서 이벤트 수신: {msg}")

            if msg.startswith("Cut_In"):
                print("🚨 침범 감지 처리됨")
                # TODO: 끼어들기 경고 음성 안내
            elif msg.startswith("Left_Deviation"):
                print("🚨 차선 좌측 치우침")
                # TODO: 좌측 치우침 경고 음성 안내
            elif msg.startswith("Right_Deviation"):
                print("🚨 차선 우측 치우침")
                # TODO: 우측 치우침 경고 음성 안내

        except Exception as e:
            print(f"⚠️ Colab WebSocket 수신 중 오류: {e}")
            colab_ws = None
            await asyncio.sleep(1)  # 재시도 대기

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
            asyncio.create_task(listen_from_colab())
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