"""
서버 상태 확인 엔드포인트

Production 환경에서 필수적인 헬스체크 API입니다.
로드밸런서, 쿠버네티스 등에서 서버 상태를 확인할 때 사용합니다.

엔드포인트:
    GET /health/         - 기본 헬스체크
    GET /health/ready    - 준비 상태 확인 (DB 연결 등)
"""

from datetime import datetime

from fastapi import APIRouter

from app.core.config import settings

# APIRouter 인스턴스
router = APIRouter()
APP_VERSION = "0.5.0"


# 헬스체크 엔드포인트
@router.get("/")
async def health_check() -> dict:
    """
    기본 헬스체크 엔드포인트

    컨테이너/로드밸런서가 애플리케이션 생존 여부를 확인할 때 사용합니다.
    """
    return {
        "status": "healthy",
        "version": APP_VERSION,
        "service": "lumi-agent",
        "environment": settings.environment,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@router.get("/ready")
async def readiness_check() -> dict:
    """
    준비 상태 확인 엔드포인트

    현재 서비스가 요청 처리 준비가 되었는지 확인합니다.
    """
    return {
        "status": "ready",
        "version": APP_VERSION,
        "service": "lumi-agent",
        "environment": settings.environment,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "checks": {
            "upstage_api_key": bool(settings.upstage_api_key),
            "supabase_configured": bool(settings.supabase_url and settings.supabase_key),
        },
    }
