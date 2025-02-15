import debugpy
import os
import uvicorn
from dotenv import load_dotenv
from app.core.app_setting import App

load_dotenv(override=True)

# SocketIO 서버 생성 (async_mode='asgi')

if os.getenv("ENV") == "dev":
    debugpy.listen(("0.0.0.0", 5678))

app = App().get_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
