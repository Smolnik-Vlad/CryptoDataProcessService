import logging

from src.core.exceptions import (BadRequestException,
                                 MethodNotAllowedException,
                                 ResourceIsForbiddenException,
                                 ResourceNotFoundException,
                                 TheServerIsFailedException,
                                 UnauthorizedAccessException,
                                 WrongConnection400_500_Exception,
                                 WrongConnection500_Exception)

logger = logging.getLogger(__name__)


async def handle_status_error(response):
    if response.status_code == 400:
        logger.warning(f"Bad request {response.status_code}")
        raise BadRequestException
    if response.status_code == 401:
        logger.warning(f"Unauthorized {response.status_code}")
        raise UnauthorizedAccessException
    if response.status_code == 403:
        logger.error(f"Forbidden {response.status_code}")
        raise ResourceIsForbiddenException
    if response.status_code == 404:
        logger.warning(f"Resource not found: {response.status_code}")
        raise ResourceNotFoundException
    if response.status_code == 405:
        logger.warning(f"Method not allowed: {response.status_code}")
        raise MethodNotAllowedException
    if response.status_code == 500:
        logger.error(f"Server failed: {response.status_code}")
        raise TheServerIsFailedException

    if 500 >= response.status_code >= 400:
        logger.error(f"Smth wrong with access (400 - 500): {response.status_code}")
        raise WrongConnection400_500_Exception

    if response.status_code >= 500:
        logger.error(
            f"Smth wrong: external server failed (500+): {response.status_code}"
        )
        raise WrongConnection500_Exception
