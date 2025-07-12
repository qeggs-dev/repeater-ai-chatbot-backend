from .._resource import (
    app,
    admin_api_key,
    chat,
    configs
)
from fastapi import (
    HTTPException,
    Header
)
from fastapi.responses import (
    JSONResponse
)
from loguru import logger

@app.post("/admin/reload/apiinfo")
async def reload_apiinfo(api_key: str = Header(..., alias="X-Admin-API-Key")):
    """
    Endpoint for reloading apiinfo
    """
    if not admin_api_key.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    logger.info("Reloading apiinfo", user_id="[Admin API]")
    await chat.reload_apiinfo()
    return JSONResponse({"detail": "Apiinfo reloaded"})

@app.post("/admin/reload/configs")
async def reload_apiinfo(api_key: str = Header(..., alias="X-Admin-API-Key")):
    """
    Endpoint for reloading apiinfo
    """
    if not admin_api_key.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    logger.info("Reloading configs", user_id="[Admin API]")
    await configs.reload_config_async()
    return JSONResponse({"detail": "Apiinfo reloaded"})


@app.post("/admin/regenerate/admin_key")
async def regenerate_admin_key(api_key: str = Header(..., alias="X-Admin-API-Key")):
    """
    Endpoint for regenerating admin key
    """
    if not admin_api_key.validate_key(api_key):
        raise HTTPException(detail="Invalid API key", status_code=401)
    logger.info("Regenerating admin key", user_id="[Admin API]")
    admin_api_key.generate()