import socketio
import asyncio
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import TypedDict
from pydantic import BaseModel, Field

from app.utils.logging import setup_logging, get_logger
from app.api.main_router import main_router
from app.services.ai.chains.chain import AIService
from app.services.chat.base import insert_chat
from app.services.chat.title.base import insert_title, make_new_title
from app.db.database import get_db

from app.schemas.chat import ChatLine


class App:
    def __init__(self):
        self.app = FastAPI(
            title="AI Chat API",
            description="FastAPI and LangChain based AI Chat Application",
            version="1.0.0",
        )

        self.logger = get_logger(__name__)
        self.client_tasks = {}
        self._setting_router()
        self._setting_socket()
        self._setting_logger()

    def _setting_socket(self):
        sio = socketio.AsyncServer(
            async_mode="asgi",
            cors_allowed_origins="*",
        )

        self.app.mount("/ws", socketio.ASGIApp(sio))

        # 연결 이벤트 핸들러
        @sio.event
        async def connect(sid, environ):
            self.logger.info(f"Client connected: {sid}")
            self.logger.info(f"environ : {environ}")

            async def send_message(sid):
                try:
                    while True:
                        await sio.sleep(3)
                        await sio.emit(
                            "response", "3초마다 전송되는 메시지입니다.", room=sid
                        )
                except asyncio.CancelledError:
                    self.logger.info(f"Task for {sid} cancelled")

            # 클라이언트 별로 태스크 생성 및 시작
            task = sio.start_background_task(send_message, sid)
            self.client_tasks[sid] = task

        # 연결 해제 이벤트 핸들러
        @sio.event
        async def disconnect(sid):
            self.logger.info(f"Client disconnected: {sid}")

            # 클라이언트 연결 해제 시 해당 태스크 취소
            task = self.client_tasks.get(sid)
            if task:
                task.cancel()
                del self.client_tasks[sid]

        # 메시지 수신 이벤트 핸들러
        @sio.on("chat")
        async def handle_message(sid, data: ChatLine):
            self.logger.info(f"Message from {sid}: {data}")
            needed_new_title = False
            key = data.get("key")
            chat_id = data.get("chat_id")
            if chat_id == "":
                needed_new_title = True
                chat_id = str(uuid4())

            writer = data.get("writer")
            message = data.get("message")

            db = next(get_db())
            await insert_chat(chat_id=chat_id, writer=writer, message=message, db=db)
            answer_chat_line = {"writer": "AI", "message": ""}
            async for value in AIService().chat(message=message):
                answer_message = value.get("answer")

                answer_chat_line.update({"message": answer_message})

                await sio.emit(
                    "chat",
                    {
                        "key": key,
                        "chat_id": chat_id,
                        "answer_chat_line": answer_chat_line,
                    },
                    room=sid,
                )
            if needed_new_title:
                title = await make_new_title(
                    first_user_question=message,
                    first_ai_answer=answer_chat_line.get("message"),
                )
                await insert_title(chat_id=chat_id, title=title, email=writer, db=db)
                await sio.emit("new_title", {"key": key, "title": title})
            await insert_chat(
                chat_id=chat_id,
                writer=answer_chat_line.get("writer"),
                message=answer_chat_line.get("message"),
                db=db,
            )

        @sio.on("new_chat_id")
        async def response_new_chat_id(sid):
            await sio.emit("new_chat_id", {"new_chat_id": uuid4()}, room=sid)

    def _setting_router(self):
        # Add main router
        self.app.include_router(main_router)

    def _setting_logger(self):
        async def startup():
            setup_logging()  # 로깅 설정은 한 번만 호출
            self.logger.info("Application startup")

        async def shutdown():
            self.logger.info("Application shutdown")

        self.app.add_event_handler("startup", startup)
        self.app.add_event_handler("shutdown", shutdown)

        # 에러 핸들러
        @self.app.exception_handler(HTTPException)
        async def http_exception_handler(request, exc):
            self.logger.error(f"HTTP error occurred: {exc.detail}")
            return {"error": exc.detail, "status_code": exc.status_code}

        @self.app.exception_handler(Exception)
        async def general_exception_handler(request, exc):
            self.logger.exception("An unexpected error occurred")
            return {"error": "Internal server error", "status_code": 500}

    def get_app(self):

        return self.app
