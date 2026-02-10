"""Search service for full-text search and filtering of tasks."""

from typing import Optional, List, Tuple
from datetime import datetime

from sqlmodel import Session, select, func, and_, or_
from sqlalchemy import text

from src.models.task import Task
from src.models.tag import Tag, TaskTag
from src.models.recurrence import TaskRecurrence
from src.schemas.search import (
    SearchQuery,
    SearchResultItem,
    SortField,
    SortOrder,
    TaskStatus,
)
from src.core.logging_config import get_logger

logger = get_logger(__name__)

# Priority sort order (higher value = more urgent)
PRIORITY_ORDER = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
    "none": 0,
    None: 0,
}


class SearchService:
    """Service for searching tasks."""

    def __init__(self, session: Session):
        self.session = session

    def search_tasks(
        self,
        user_id: str,
        query: SearchQuery
    ) -> Tuple[List[SearchResultItem], int, bool]:
        """Search tasks with filters and full-text search.

        Args:
            user_id: The user ID
            query: Search query parameters

        Returns:
            Tuple of (results, total_count, has_more)
        """
        # Build base query
        statement = select(Task).where(Task.user_id == user_id)
        count_statement = select(func.count()).select_from(Task).where(Task.user_id == user_id)

        # Apply filters
        statement, count_statement = self._apply_filters(
            statement, count_statement, query, user_id
        )

        # Get total count before pagination
        total = self.session.exec(count_statement).one()

        # Apply sorting
        statement = self._apply_sorting(statement, query)

        # Apply pagination
        statement = statement.offset(query.offset).limit(query.limit + 1)  # +1 to check has_more

        # Execute query
        tasks = list(self.session.exec(statement).all())

        # Check if there are more results
        has_more = len(tasks) > query.limit
        if has_more:
            tasks = tasks[:query.limit]

        # Enrich results with tags and recurrence info
        results = []
        for task in tasks:
            result = self._enrich_task(task)
            results.append(result)

        logger.info(f"Search returned {len(results)} of {total} results for user {user_id}")
        return results, total, has_more

    def _apply_filters(
        self,
        statement,
        count_statement,
        query: SearchQuery,
        user_id: str
    ):
        """Apply search filters to the query."""

        # Full-text search
        if query.text:
            search_term = query.text.strip()
            if search_term:
                # Use ILIKE for simple search (works without tsvector)
                # TODO: Use tsvector when search_vector column is populated
                search_pattern = f"%{search_term}%"
                search_condition = or_(
                    Task.title.ilike(search_pattern),
                    Task.description.ilike(search_pattern) if hasattr(Task, 'description') else False
                )
                statement = statement.where(search_condition)
                count_statement = count_statement.where(search_condition)

        # Status filter
        if query.status:
            status_conditions = []
            for status in query.status:
                if status == TaskStatus.COMPLETED:
                    status_conditions.append(Task.completed == True)
                elif status == TaskStatus.PENDING:
                    status_conditions.append(Task.completed == False)

            if status_conditions:
                statement = statement.where(or_(*status_conditions))
                count_statement = count_statement.where(or_(*status_conditions))

        # Priority filter
        if query.priority and hasattr(Task, 'priority'):
            priority_values = [p.value for p in query.priority]
            statement = statement.where(Task.priority.in_(priority_values))
            count_statement = count_statement.where(Task.priority.in_(priority_values))

        # Due date range
        if query.due_date_from and hasattr(Task, 'due_date'):
            statement = statement.where(Task.due_date >= query.due_date_from)
            count_statement = count_statement.where(Task.due_date >= query.due_date_from)

        if query.due_date_to and hasattr(Task, 'due_date'):
            statement = statement.where(Task.due_date <= query.due_date_to)
            count_statement = count_statement.where(Task.due_date <= query.due_date_to)

        # Tag filter
        if query.tags:
            # Subquery to find tasks with matching tags
            tag_subquery = (
                select(TaskTag.task_id)
                .where(TaskTag.tag_id.in_(query.tags))
                .distinct()
            )
            statement = statement.where(Task.id.in_(tag_subquery))
            count_statement = count_statement.where(Task.id.in_(tag_subquery))

        # Recurrence filter
        if query.has_recurrence is not None:
            recurrence_subquery = (
                select(TaskRecurrence.task_id)
                .where(TaskRecurrence.is_active == True)
                .distinct()
            )
            if query.has_recurrence:
                statement = statement.where(Task.id.in_(recurrence_subquery))
                count_statement = count_statement.where(Task.id.in_(recurrence_subquery))
            else:
                statement = statement.where(Task.id.notin_(recurrence_subquery))
                count_statement = count_statement.where(Task.id.notin_(recurrence_subquery))

        return statement, count_statement

    def _apply_sorting(self, statement, query: SearchQuery):
        """Apply sorting to the query."""

        if query.sort_by == SortField.RELEVANCE:
            # For relevance, sort by created_at as fallback
            # TODO: Implement proper relevance ranking with tsvector
            if query.sort_order == SortOrder.DESC:
                statement = statement.order_by(Task.created_at.desc())
            else:
                statement = statement.order_by(Task.created_at.asc())

        elif query.sort_by == SortField.DUE_DATE:
            if hasattr(Task, 'due_date'):
                # Null due dates go last
                if query.sort_order == SortOrder.ASC:
                    statement = statement.order_by(
                        Task.due_date.asc().nullslast()
                    )
                else:
                    statement = statement.order_by(
                        Task.due_date.desc().nullsfirst()
                    )
            else:
                statement = statement.order_by(Task.created_at.desc())

        elif query.sort_by == SortField.PRIORITY:
            # Custom sorting by priority weight
            if hasattr(Task, 'priority'):
                # Use CASE expression for custom priority order
                priority_case = func.coalesce(
                    func.nullif(Task.priority, None),
                    'none'
                )
                if query.sort_order == SortOrder.DESC:
                    statement = statement.order_by(
                        priority_case.desc(),
                        Task.created_at.desc()
                    )
                else:
                    statement = statement.order_by(
                        priority_case.asc(),
                        Task.created_at.asc()
                    )
            else:
                statement = statement.order_by(Task.created_at.desc())

        elif query.sort_by == SortField.CREATED_AT:
            if query.sort_order == SortOrder.DESC:
                statement = statement.order_by(Task.created_at.desc())
            else:
                statement = statement.order_by(Task.created_at.asc())

        elif query.sort_by == SortField.TITLE:
            if query.sort_order == SortOrder.ASC:
                statement = statement.order_by(Task.title.asc())
            else:
                statement = statement.order_by(Task.title.desc())

        return statement

    def _enrich_task(self, task: Task) -> SearchResultItem:
        """Enrich task with additional data (tags, recurrence)."""

        # Get tags
        tags_statement = (
            select(Tag)
            .join(TaskTag, Tag.id == TaskTag.tag_id)
            .where(TaskTag.task_id == task.id)
        )
        tags = list(self.session.exec(tags_statement).all())
        tag_dicts = [
            {"id": t.id, "name": t.name, "color": t.color}
            for t in tags
        ]

        # Check for recurrence
        recurrence_statement = select(TaskRecurrence).where(
            TaskRecurrence.task_id == task.id,
            TaskRecurrence.is_active == True
        )
        has_recurrence = self.session.exec(recurrence_statement).first() is not None

        return SearchResultItem(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description if hasattr(task, 'description') else None,
            completed=task.completed,
            priority=task.priority if hasattr(task, 'priority') else None,
            due_date=task.due_date if hasattr(task, 'due_date') else None,
            created_at=task.created_at,
            updated_at=task.updated_at,
            tags=tag_dicts,
            has_recurrence=has_recurrence,
        )

    def quick_search(
        self,
        user_id: str,
        text: str,
        limit: int = 5
    ) -> dict:
        """Quick search for autocomplete.

        Args:
            user_id: The user ID
            text: Search text
            limit: Max results per category

        Returns:
            Dict with 'tasks' and 'tags' lists
        """
        search_pattern = f"%{text.strip()}%"

        # Search tasks
        task_statement = (
            select(Task)
            .where(
                Task.user_id == user_id,
                Task.title.ilike(search_pattern)
            )
            .order_by(Task.created_at.desc())
            .limit(limit)
        )
        tasks = list(self.session.exec(task_statement).all())
        task_results = [
            {
                "id": t.id,
                "title": t.title,
                "completed": t.completed,
            }
            for t in tasks
        ]

        # Search tags
        tag_statement = (
            select(Tag)
            .where(
                Tag.user_id == user_id,
                Tag.name.ilike(search_pattern)
            )
            .order_by(Tag.usage_count.desc())
            .limit(limit)
        )
        tags = list(self.session.exec(tag_statement).all())
        tag_results = [
            {
                "id": t.id,
                "name": t.name,
                "color": t.color,
            }
            for t in tags
        ]

        return {
            "tasks": task_results,
            "tags": tag_results,
        }
