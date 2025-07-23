import yt_dlp
import tempfile
import os
from typing import Dict, Any, Optional


class TwitterVideoExtractor:
    @staticmethod
    def extract(url: str, cookies: Optional[str] = None) -> Dict[str, Any]:
        ydl_opts = {
            "format": "best[ext=mp4]",
            "quiet": True,
        }

        # 쿠키 처리
        if cookies:
            temp_cookies_file = tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".txt"
            )
            temp_cookies_file.write(cookies)
            temp_cookies_file.close()
            ydl_opts["cookiefile"] = temp_cookies_file.name

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                # 임시 쿠키 파일 삭제
                if cookies and "cookiefile" in ydl_opts:
                    os.unlink(ydl_opts["cookiefile"])

                return {
                    "success": True,
                    "title": info.get("title"),
                    "uploader": info.get("uploader"),
                    "duration": info.get("duration"),
                    "thumbnail": info.get("thumbnail"),
                    "stream_url": info.get("url"),
                    "formats": [
                        {
                            "quality": fmt.get("format_note", "Unknown"),
                            "url": fmt.get("url"),
                            "filesize": fmt.get("filesize"),
                        }
                        for fmt in info.get("formats", [])[-5:]  # 최근 5개 화질
                    ],
                }

        except Exception as e:
            return {"success": False, "error": str(e)}
