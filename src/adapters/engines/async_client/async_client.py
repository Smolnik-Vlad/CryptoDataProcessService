import logging
from typing import AsyncGenerator

import httpx

from src.adapters.engines.async_client.status_errors import handle_status_error
from src.core.exceptions import (ConnectionErrorException,
                                 RequestAvailableException,
                                 RequestTimeoutException)

logger = logging.getLogger(__name__)


async def get_async_client() -> AsyncGenerator:
    event_hooks = {"response": [handle_status_error]}
    try:
        async with httpx.AsyncClient(event_hooks=event_hooks) as client:
            yield client
    except httpx.TimeoutException as e:
        logger.error(f"Request timed out {e.request}")
        raise RequestTimeoutException
    except httpx.RequestError as e:
        logger.error(f"Unable to connect: {e.request}")
        raise RequestAvailableException
    except httpx.ConnectError as e:
        logger.error(f"Unable to connect: {e.request}")
        raise ConnectionErrorException
