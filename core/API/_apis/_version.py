from .._resource import app
from .._info import __version__ as __api_version__
from ..._core import __version__ as __core_version__
from fastapi.responses import (
    ORJSONResponse,
    PlainTextResponse
)

@app.route('/version')
def version():
    """
    Return the version of the API and the core
    """
    return ORJSONResponse(
        {
        'core': __core_version__,
        'api': __api_version__
        }
    )

@app.route('/version/core')
def core_version():
    """
    Return the version of the core
    """
    return PlainTextResponse(
        __core_version__
    )

@app.route('/version/api')
def api_version():
    """
    Return the version of the API
    """
    return PlainTextResponse(
        __api_version__
    )
