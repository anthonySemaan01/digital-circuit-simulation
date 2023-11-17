"""
Endpoint for checking the health of the API server.

The prefix endpoint is '/health'
"""
from fastapi import APIRouter
from starlette.responses import Response

router = APIRouter()


@router.get("")
def health():
    """
    Check server health.

    Endpoint: '/health'
    """
    return Response(status_code=200)
