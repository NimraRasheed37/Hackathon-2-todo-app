"""Search API routes."""

from fastapi import APIRouter, Query, status

from src.api.dependencies import CurrentUserDep, SessionDep
from src.core.logging_config import get_logger
from src.core.security import validate_user_authorization
from src.schemas.search import SearchQuery, SearchResults, QuickSearchResult
from src.services.search_service import SearchService

router = APIRouter()
logger = get_logger(__name__)


def get_search_service(session: SessionDep) -> SearchService:
    """Get SearchService instance with injected session."""
    return SearchService(session)


@router.post(
    "/{user_id}/tasks/search",
    response_model=SearchResults,
)
async def search_tasks(
    user_id: str,
    query: SearchQuery,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    """Search tasks with filters and full-text search.

    Supports:
    - Full-text search on title and description
    - Filtering by status, priority, tags, due date range
    - Filtering by recurrence status
    - Multiple sort options
    - Pagination
    """
    validate_user_authorization(current_user.id, user_id)

    service = get_search_service(session)
    results, total, has_more = service.search_tasks(user_id, query)

    return SearchResults(
        results=results,
        total=total,
        has_more=has_more,
        query=query.model_dump(),
    )


@router.get(
    "/{user_id}/tasks/quick-search",
    response_model=QuickSearchResult,
)
async def quick_search(
    user_id: str,
    q: str = Query(min_length=1, max_length=100),
    limit: int = Query(default=5, ge=1, le=10),
    current_user: CurrentUserDep = None,
    session: SessionDep = None,
):
    """Quick search for autocomplete.

    Returns matching tasks and tags for the search term.
    """
    validate_user_authorization(current_user.id, user_id)

    service = get_search_service(session)
    results = service.quick_search(user_id, q, limit)

    return QuickSearchResult(
        tasks=results["tasks"],
        tags=results["tags"],
    )
