from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging import setup_logging, get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="AI Chat API",
    description="FastAPI and LangChain based AI Chat Application",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 실제 도메인으로 변경
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 시작 시 이벤트
@app.on_event("startup")
async def startup_event():
    setup_logging()
    logger.info("Application startup")

# 종료 시 이벤트
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")

# 헬스체크 엔드포인트
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 루트 엔드포인트
@app.get("/")
async def root():
    return {
        "message": "Welcome to AI Chat API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

# 에러 핸들러
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error occurred: {exc.detail}")
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.exception("An unexpected error occurred")
    return {
        "error": "Internal server error",
        "status_code": 500
    }