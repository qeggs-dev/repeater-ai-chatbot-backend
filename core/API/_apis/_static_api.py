from .._resource import app
from fastapi.responses import FileResponse

from ...Global_Config_Manager import configs

static_dir = configs.static.static_dir

@app.get('/favicon.ico')
async def favicon_ico():
    """Return favicon"""
    return FileResponse(f'{static_dir}/favicon.ico')

@app.get('/favicon.png')
async def favicon_png():
    """Return favicon"""
    return FileResponse(f'{static_dir}/favicon.png')

@app.get('/favicon.svg')
async def favicon_svg():
    """Return favicon"""
    return FileResponse(f'{static_dir}/favicon.svg')

@app.get('/robots.txt')
async def robots():
    """Return robots.txt"""
    return FileResponse(f'{static_dir}/robots.txt')

@app.get('/static/{path:path}')
async def static(path: str):
    """Return static files"""
    return FileResponse(f'{static_dir}/{path}')