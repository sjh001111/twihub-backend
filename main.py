from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ExtractRequest, ExtractResponse, VideoFormat
from video_extractor import TwitterVideoExtractor
import uvicorn

app = FastAPI(
    title="Twitter Video Downloader API",
    description="트위터 동영상 추출 및 다운로드 API",
    version="1.0.0",
)

# CORS 설정 (Next.js와 연동을 위해)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js 기본 포트
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Twitter Video Downloader API", "status": "running"}


@app.post("/extract", response_model=ExtractResponse)
async def extract_video(request: ExtractRequest):
    """
    트위터 동영상 정보 추출
    """
    try:
        # URL 유효성 간단 체크
        if not ("twitter.com" in request.url or "x.com" in request.url):
            raise HTTPException(status_code=400, detail="유효한 트위터 URL이 아닙니다.")

        # 동영상 정보 추출
        result = TwitterVideoExtractor.extract(request.url, request.cookies)

        if not result["success"]:
            # NSFW 또는 인증 필요한 경우
            if (
                "authentication" in result["error"].lower()
                or "nsfw" in result["error"].lower()
            ):
                return ExtractResponse(
                    success=False,
                    error="NSFW 또는 비공개 트윗입니다. 쿠키가 필요합니다.",
                )
            else:
                return ExtractResponse(success=False, error=result["error"])

        # 성공 응답
        return ExtractResponse(
            success=True,
            title=result["title"],
            uploader=result["uploader"],
            duration=result["duration"],
            thumbnail=result["thumbnail"],
            stream_url=result["stream_url"],
            formats=[
                VideoFormat(
                    quality=fmt["quality"], url=fmt["url"], filesize=fmt["filesize"]
                )
                for fmt in result["formats"]
            ],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@app.get("/health")
async def health_check():
    """서버 상태 체크"""
    return {"status": "healthy", "message": "API is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
