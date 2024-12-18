import logging
import sys
from pathlib import Path
from loguru import logger
from datetime import datetime

# 로그 파일 경로 설정
LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# 로그 파일명 형식 설정
log_filename = f"{datetime.now().strftime('%Y-%m-%d')}.log"
log_filepath = LOG_DIR / log_filename

# Loguru 설정
config = {
    "handlers": [
        # 콘솔 출력 핸들러
        {
            "sink": sys.stdout,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            "level": "INFO",
        },
        # 파일 출력 핸들러
        {
            "sink": str(log_filepath),
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
            "level": "DEBUG",
            "rotation": "00:00",  # 매일 자정에 새로운 파일 생성
            "retention": "30 days",  # 30일간 로그 보관
            "compression": "zip",  # 이전 로그 파일 압축
        },
    ],
}

# Loguru 설정 적용
logger.configure(**config)

# FastAPI 로깅과 통합
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Retrieve context where the logging call occurred, this happens to be in the 6th frame upward
        try:
            frame = sys._getframe(6)
        except ValueError:
            frame = None

        # Get caller from frame
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())

# FastAPI 로깅 설정
def setup_logging():
    # 기존 로거 제거
    logging.getLogger().handlers = []
    
    # 로깅 핸들러 설정
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    
    # 특정 모듈의 로깅 레벨 설정
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.error").handlers = [InterceptHandler()]

# 로거 가져오기 함수
def get_logger(name: str) -> logger:
    """
    지정된 이름으로 로거를 반환합니다.
    
    Args:
        name (str): 로거 이름 (보통 __name__ 사용)
        
    Returns:
        logger: 설정된 로거 인스턴스
    """
    return logger.bind(name=name)