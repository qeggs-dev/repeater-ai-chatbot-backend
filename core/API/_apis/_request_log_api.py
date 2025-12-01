from .._resource import chat, app
import orjson
from typing import AsyncIterator
from fastapi.responses import JSONResponse, StreamingResponse

@app.get("/request_log")
@app.get("/request_log/list")
async def get_request_log():
    """
    Endpoint for getting request log
    
    Args:
        filter: Optional list of filters
    
    Returns:
        JSONResponse: Filtered log object dictionary
    """
    logs = await chat.request_log.read_request_log()
    return JSONResponse(logs)

@app.get("/request_log/stream")
async def stream_request_log():
    """
    流式传输通话日志
    
    Args:
        filter: Optional list of filters
    
    Returns:
        StreamingResponse: Filtered log object dictionary
    """
    async def generate_jsonl() -> AsyncIterator[bytes]:
        """生成JSONL格式的字节流"""
        async for log in chat.request_log.read_stream_request_log():
            yield orjson.dumps(log) + b"\n"

    return StreamingResponse(
        generate_jsonl(),
        media_type="application/x-ndjson",
        headers={
            "X-Content-Type-Options": "nosniff",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )