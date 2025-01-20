import uvicorn
from app.core.app_setting import App

# SocketIO 서버 생성 (async_mode='asgi')


app = App().get_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
