import yt_dlp
import json


def test_twitter_with_auth(url):
    """트위터 계정 인증 포함 테스트"""
    print(f"테스트 URL: {url}")
    print("-" * 50)

    ydl_opts = {
        "format": "best[ext=mp4]",
        "cookiefile": "cookies.txt",
        "quiet": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            print("✅ 추출 성공!")
            print(f"제목: {info.get('title', 'N/A')}")
            print(f"업로더: {info.get('uploader', 'N/A')}")
            print(f"재생시간: {info.get('duration', 'N/A')}초")
            print(f"조회수: {info.get('view_count', 'N/A')}")
            print(f"스트림 URL: {info.get('url', 'N/A')[:100]}...")  # URL 앞부분만
            print(f"썸네일: {info.get('thumbnail', 'N/A')}")

            # 화질 옵션들
            if "formats" in info:
                print(f"\n사용 가능한 화질 수: {len(info['formats'])}")
                for fmt in info["formats"][-3:]:
                    resolution = fmt.get("resolution", "Unknown")
                    filesize = fmt.get("filesize", "Unknown")
                    print(f"  - {resolution}: {filesize} bytes")

            return info

    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        return None


if __name__ == "__main__":
    # 이전 NSFW 트윗으로 다시 테스트
    test_url = "https://x.com/robert_v_mill/status/1946933291468398847"

    result = test_twitter_with_auth(test_url)
