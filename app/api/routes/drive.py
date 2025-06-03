import os
import ssl
import asyncio
import websockets
from fastapi import Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_user
from app.schemas.drive_history import DriveScoreResponse
from app.services import drive_score_service
from app.crud import drive_history_crud

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


@router.get("/score", response_model=DriveScoreResponse)
def get_drive_score_report(
    db: Session = Depends(get_db),
    user=Depends(get_user)
):
    # 1. 유저 이력 불러오기
    histories = drive_history_crud.get_drive_histories_by_user_id(db, user.user_id)
    if not histories:
        return DriveScoreResponse(latest_score=0.0, percentile=0.0, monthly_scores={})

    # ✅ 2. 최신 기록 가져오기 (start_at 기준으로 가장 최근)
    latest_history = max(histories, key=lambda h: h.start_at)
    latest_score = latest_history.score

    # ✅ 전체 유저 중, 유저당 가장 최신 기록만 사용
    all_histories = db.query(drive_history_crud.DriveHistory).filter(
        drive_history_crud.DriveHistory.score.isnot(None)).all()
    latest_by_user = {}

    for h in all_histories:
       if h.user_id not in latest_by_user or h.start_at > latest_by_user[h.user_id].start_at:
            latest_by_user[h.user_id] = h

    # ✅ 내 user_id는 무시하고, 내 점수는 한 번만 따로 넣기
    all_scores = [float(h.score) for uid, h in latest_by_user.items() if uid != user.user_id]
    all_scores.append(float(latest_score))

    percentile = drive_score_service.calculate_percentile(latest_score, all_scores)

    # 4. 월별 평균 점수 계산 (DB score 값 기준)
    monthly_scores = drive_score_service.calculate_monthly_scores(histories)

    return DriveScoreResponse(
        latest_score=latest_score,
        percentile=percentile,
        monthly_scores=monthly_scores
    )


@router.get("/devtest", response_model=DriveScoreResponse)
def get_drive_score_devtest(db: Session = Depends(get_db)):
    #  user_id 3 강제 지정 (임시용)
    user_id = 3

    histories = drive_history_crud.get_drive_histories_by_user_id(db, user_id)
    if not histories:
        return DriveScoreResponse(latest_score=0.0, percentile=0.0, monthly_scores={})

    latest_history = max(histories, key=lambda h: h.start_at)  # ✅ start_at 기준 최신 기록
    latest_score = latest_history.score

    # ✅ 전체 유저당 가장 최신 이력만 추출
    all_histories = db.query(drive_history_crud.DriveHistory).filter(
        drive_history_crud.DriveHistory.score.isnot(None)
    ).all()

    latest_by_user = {}
    for h in all_histories:
        if h.user_id not in latest_by_user or h.start_at > latest_by_user[h.user_id].start_at:
            latest_by_user[h.user_id] = h

    all_scores = [float(h.score) for uid, h in latest_by_user.items() if uid != user_id]
    all_scores.append(float(latest_score))  # 내 점수는 한 번만 포함

    percentile = drive_score_service.calculate_percentile(latest_score, all_scores)
    monthly_scores = drive_score_service.calculate_monthly_scores(histories)

    return DriveScoreResponse(
        latest_score=latest_score,
        percentile=percentile,
        monthly_scores=monthly_scores
    )
