from pydantic import BaseModel
from typing import Optional, List

class ExtractRequest(BaseModel):
    url: str
    cookies: Optional[str] = None

class VideoFormat(BaseModel):
    quality: str
    url: str
    filesize: Optional[int] = None

class ExtractResponse(BaseModel):
    success: bool
    title: Optional[str] = None
    uploader: Optional[str] = None
    duration: Optional[int] = None
    thumbnail: Optional[str] = None
    stream_url: Optional[str] = None
    formats: Optional[List[VideoFormat]] = None
    error: Optional[str] = None