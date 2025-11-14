from .._resource import app, configs
from fastapi.responses import FileResponse

@app.get('/favicon.ico')
async def favicon():
    """Return favicon"""
    static_dir = configs.get_config('static.base_path').get_value(str)
    return FileResponse(f'{static_dir}/favicon.ico')

@app.get('/static/{path:path}')
async def static(path: str):
    """Return static files"""
    static_dir = configs.get_config('static.base_path').get_value(str)
    return FileResponse(f'{static_dir}/{path}')