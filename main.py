import base64
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

from video_extractor import TwitterVideoExtractor

# https://x.com/robert_v_mill/status/1946933291468398847

load_dotenv()
cookies_b64 = os.getenv("TWITTER_COOKIES_B64")
cookies = base64.b64decode(cookies_b64).decode()

app = FastAPI(
    title="Twitter Video Downloader API",
    description="트위터 동영상 추출 및 다운로드 API",
    version="1.0.0",
)

# CORS 설정 (Next.js와 연동을 위해)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://twihub-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Twitter Video Downloader API", "status": "running"}


@app.post("/extract")
async def extract_video(url: str = Form(...)):
    print(url)
    try:
        # URL 유효성 간단 체크
        # if not ("twitter.com" in url or "x.com" in url):
        #     raise HTTPException(status_code=400, detail="유효한 트위터 URL이 아닙니다.")

        # 쿠키는 환경변수에서 자동으로 가져옴 (None 전달)
        result = TwitterVideoExtractor.extract(url, cookies)

        if not result["success"]:
            return {"success": False, "error": result["error"]}

        return {
            "success": True,
            "title": result["title"],
            "uploader": result["uploader"],
            "duration": result["duration"],
            "thumbnail": result["thumbnail"],
            "stream_url": result["stream_url"],
            "formats": result["formats"],
        }

    except Exception as e:
        return {"success": False, "error": f"서버 오류: {str(e)}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
