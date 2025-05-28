import os

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import base64
import requests

router = APIRouter(prefix="/drive", tags=["drive"])


def send_frame_to_colab_direct(image_bytes: bytes) -> str:
    url = os.getenv("COLAB_NGROK_URL")  # TODO: 실제 주소로 변경
    files = {"file": ("frame.jpg", image_bytes, "image/jpeg")}

    try:
        response = requests.post(url, files=files, timeout=10)
        response.raise_for_status()
        return response.json().get("result", "결과 없음")
    except Exception as e:
        return f"Colab 전송 실패: {e}"


@router.websocket("/ws/video")
async def websocket_video(websocket: WebSocket):
    await websocket.accept()
    print("✅ WebSocket 연결됨")

    try:
        while True:
            data = await websocket.receive_text()  # base64 문자열 수신
            img_data = base64.b64decode(data)

            send_frame_to_colab_direct(img_data)

    except WebSocketDisconnect:
        print("❌ WebSocket 연결 종료됨")
    except Exception as e:
        print(f"⚠️ 예외 발생: {e}")
