from typing import List
from openai import AsyncOpenAI
from openai.types.image import Image
from openai.types.images_response import ImagesResponse
from loguru import logger
from ...Coroutine_Pool import CoroutinePool
from ._request import Request, ImageSize
from ._response import Response

class ImageAPI:
    def __init__(self, max_concurrency:int = 10):
        self._coroutine_pool = CoroutinePool(max_concurrency = max_concurrency)
        self._max_concurrency = max_concurrency
    
    async def _create_image(self, request: Request) -> Response:
        client = AsyncOpenAI(
            base_url = request.base_url,
            api_key = request.api_key,
        )

        if isinstance(request.size, ImageSize):
            request_size = request.size.value
        else:
            request_size = request.size
        response: ImagesResponse = await client.images.generate(
            model = request.model,
            prompt = request.prompt,
            n = request.n,
            size = request_size,
        )

        images: list[str] = []
        data: List[Image] | None = response.data
        for image in data:
            images.append(image.url)
        
        return Response(
            created = response.created,
            images = images,
        )
    
    async def submit(self, request: Request) -> Response:
        return await self._coroutine_pool.submit(
            self._create_image(request = request)
        )