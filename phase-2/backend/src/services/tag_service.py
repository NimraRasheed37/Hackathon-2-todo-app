"""Tag service for managing user tags and task-tag associations."""

from typing import Optional, List

from sqlmodel import Session, select, func

from src.models.tag import Tag, TaskTag
from src.schemas.tag import TagCreate, TagUpdate
from src.core.logging_config import get_logger

logger = get_logger(__name__)


class TagService:
    """Service for managing tags."""

    def __init__(self, session: Session):
        self.session = session

    def create_tag(self, user_id: str, tag_data: TagCreate) -> Tag:
        """Create a new tag for a user.

        Args:
            user_id: The user ID
            tag_data: Tag creation data

        Returns:
            The created Tag

        Raises:
            ValueError: If tag with same name exists for user
        """
        # Check if tag with same name exists
        existing = self.get_tag_by_name(user_id, tag_data.name)
        if existing:
            raise ValueError(f"Tag '{tag_data.name}' already exists")

        tag = Tag(
            user_id=user_id,
            name=tag_data.name,
            color=tag_data.color,
            icon=tag_data.icon,
            usage_count=0,
        )

        self.session.add(tag)
        self.session.commit()
        self.session.refresh(tag)

        logger.info(f"Created tag {tag.id} '{tag.name}' for user {user_id}")
        return tag

    def get_tag(self, tag_id: int) -> Optional[Tag]:
        """Get a tag by ID."""
        return self.session.get(Tag, tag_id)

    def get_tag_by_name(self, user_id: str, name: str) -> Optional[Tag]:
        """Get a tag by name for a user."""
        statement = select(Tag).where(
            Tag.user_id == user_id,
            func.lower(Tag.name) == name.lower()
        )
        return self.session.exec(statement).first()

    def get_user_tags(
        self,
        user_id: str,
        sort_by: str = "name"
    ) -> List[Tag]:
        """Get all tags for a user.

        Args:
            user_id: The user ID
            sort_by: Sort field ('name', 'usage', 'created')

        Returns:
            List of tags
        """
        statement = select(Tag).where(Tag.user_id == user_id)

        if sort_by == "usage":
            statement = statement.order_by(Tag.usage_count.desc())
        elif sort_by == "created":
            statement = statement.order_by(Tag.created_at.desc())
        else:
            statement = statement.order_by(Tag.name)

        return list(self.session.exec(statement).all())

    def update_tag(
        self,
        tag_id: int,
        user_id: str,
        tag_data: TagUpdate
    ) -> Optional[Tag]:
        """Update a tag.

        Args:
            tag_id: The tag ID
            user_id: The user ID (for authorization)
            tag_data: Tag update data

        Returns:
            The updated tag or None if not found/unauthorized
        """
        tag = self.session.get(Tag, tag_id)
        if not tag or tag.user_id != user_id:
            return None

        # Check for name conflict if name is being changed
        if tag_data.name and tag_data.name.lower() != tag.name.lower():
            existing = self.get_tag_by_name(user_id, tag_data.name)
            if existing:
                raise ValueError(f"Tag '{tag_data.name}' already exists")

        if tag_data.name is not None:
            tag.name = tag_data.name
        if tag_data.color is not None:
            tag.color = tag_data.color
        if tag_data.icon is not None:
            tag.icon = tag_data.icon

        self.session.add(tag)
        self.session.commit()
        self.session.refresh(tag)

        logger.info(f"Updated tag {tag_id}")
        return tag

    def delete_tag(self, tag_id: int, user_id: str) -> bool:
        """Delete a tag and remove it from all tasks.

        Args:
            tag_id: The tag ID
            user_id: The user ID (for authorization)

        Returns:
            True if deleted, False if not found/unauthorized
        """
        tag = self.session.get(Tag, tag_id)
        if not tag or tag.user_id != user_id:
            return False

        # Delete task-tag associations
        statement = select(TaskTag).where(TaskTag.tag_id == tag_id)
        associations = list(self.session.exec(statement).all())
        for assoc in associations:
            self.session.delete(assoc)

        # Delete the tag
        self.session.delete(tag)
        self.session.commit()

        logger.info(f"Deleted tag {tag_id} and removed from {len(associations)} tasks")
        return True

    def get_task_tags(self, task_id: int) -> List[Tag]:
        """Get all tags for a task."""
        statement = (
            select(Tag)
            .join(TaskTag, Tag.id == TaskTag.tag_id)
            .where(TaskTag.task_id == task_id)
            .order_by(Tag.name)
        )
        return list(self.session.exec(statement).all())

    def set_task_tags(
        self,
        task_id: int,
        tag_ids: List[int],
        user_id: str
    ) -> List[Tag]:
        """Set tags for a task (replaces existing tags).

        Args:
            task_id: The task ID
            tag_ids: List of tag IDs to assign
            user_id: The user ID (for authorization)

        Returns:
            List of assigned tags
        """
        # Remove existing tags
        statement = select(TaskTag).where(TaskTag.task_id == task_id)
        existing = list(self.session.exec(statement).all())
        for assoc in existing:
            self.session.delete(assoc)

        # Add new tags
        assigned_tags = []
        for tag_id in tag_ids:
            tag = self.session.get(Tag, tag_id)
            if tag and tag.user_id == user_id:
                assoc = TaskTag(task_id=task_id, tag_id=tag_id)
                self.session.add(assoc)
                assigned_tags.append(tag)

                # Update usage count
                tag.usage_count += 1
                self.session.add(tag)

        self.session.commit()

        logger.info(f"Set {len(assigned_tags)} tags for task {task_id}")
        return assigned_tags

    def add_tag_to_task(
        self,
        task_id: int,
        tag_id: int,
        user_id: str
    ) -> Optional[Tag]:
        """Add a single tag to a task.

        Args:
            task_id: The task ID
            tag_id: The tag ID
            user_id: The user ID (for authorization)

        Returns:
            The added tag or None if not found/unauthorized
        """
        tag = self.session.get(Tag, tag_id)
        if not tag or tag.user_id != user_id:
            return None

        # Check if already assigned
        statement = select(TaskTag).where(
            TaskTag.task_id == task_id,
            TaskTag.tag_id == tag_id
        )
        if self.session.exec(statement).first():
            return tag  # Already assigned

        assoc = TaskTag(task_id=task_id, tag_id=tag_id)
        self.session.add(assoc)

        # Update usage count
        tag.usage_count += 1
        self.session.add(tag)

        self.session.commit()

        logger.info(f"Added tag {tag_id} to task {task_id}")
        return tag

    def remove_tag_from_task(
        self,
        task_id: int,
        tag_id: int,
        user_id: str
    ) -> bool:
        """Remove a tag from a task.

        Args:
            task_id: The task ID
            tag_id: The tag ID
            user_id: The user ID (for authorization)

        Returns:
            True if removed, False if not found
        """
        tag = self.session.get(Tag, tag_id)
        if not tag or tag.user_id != user_id:
            return False

        statement = select(TaskTag).where(
            TaskTag.task_id == task_id,
            TaskTag.tag_id == tag_id
        )
        assoc = self.session.exec(statement).first()
        if not assoc:
            return False

        self.session.delete(assoc)

        # Update usage count
        if tag.usage_count > 0:
            tag.usage_count -= 1
            self.session.add(tag)

        self.session.commit()

        logger.info(f"Removed tag {tag_id} from task {task_id}")
        return True
