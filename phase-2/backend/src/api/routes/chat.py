"""Chat API routes for AI-powered task management."""

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from src.agents.task_agent import TaskAgent
from src.agents.tools import create_tool_executor
from src.api.dependencies import get_current_user
from src.config import get_settings
from src.core.logging_config import get_logger
from src.database import get_session
from src.repositories.conversation_repository import ConversationRepository
from src.schemas.auth import UserInfo
from src.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationDetail,
    ConversationSummary,
    MessageRead,
    ToolCallResult,
)

logger = get_logger(__name__)
settings = get_settings()

router = APIRouter()

# Type aliases for dependency injection
SessionDep = Annotated[Session, Depends(get_session)]
CurrentUserDep = Annotated[UserInfo, Depends(get_current_user)]


@router.post("/chat", response_model=ChatResponse)
async def send_chat_message(
    request: ChatRequest,
    session: SessionDep,
    current_user: CurrentUserDep,
):
    """
    Send a message to the AI assistant.

    The assistant can create, list, complete, delete, or update tasks
    through natural conversation.
    """
    user_id = current_user.id

    # Validate message
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    if len(request.message) > 2000:
        raise HTTPException(status_code=400, detail="Message cannot exceed 2000 characters")

    # Check if OpenAI is configured
    if not settings.openai_api_key:
        raise HTTPException(
            status_code=503,
            detail="AI service is not configured. Please set OPENAI_API_KEY."
        )

    conv_repo = ConversationRepository(session)

    # Load or create conversation
    if request.conversation_id:
        conversation = conv_repo.get_by_id_and_user(request.conversation_id, user_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        # Create new conversation with title from first message
        title = request.message[:50] + "..." if len(request.message) > 50 else request.message
        conversation = conv_repo.create(user_id, title=title)
        logger.info(f"Created new conversation {conversation.id} for user {user_id}")

    # Load conversation history (last 50 messages)
    messages = conv_repo.get_messages(
        conversation.id,
        limit=settings.max_conversation_messages
    )

    # Convert to OpenAI format
    conversation_history = []
    for msg in messages:
        if msg.role == "tool":
            # Skip tool messages - they're part of the assistant's context
            continue
        conversation_history.append({
            "role": msg.role,
            "content": msg.content,
        })

    # Save user message
    conv_repo.add_message(conversation.id, "user", request.message)

    try:
        # Create tool executor and agent
        tool_executor = create_tool_executor(session, user_id)
        agent = TaskAgent(tool_executor)

        # Get AI response
        response_text, tool_calls_made = agent.chat(
            request.message,
            conversation_history,
        )

        # Save assistant response
        tool_calls_data = None
        if tool_calls_made:
            tool_calls_data = {"calls": tool_calls_made}

        conv_repo.add_message(
            conversation.id,
            "assistant",
            response_text,
            tool_calls=tool_calls_data,
        )

        # Format response
        formatted_tool_calls = None
        if tool_calls_made:
            formatted_tool_calls = [
                ToolCallResult(
                    name=tc["name"],
                    arguments=tc["arguments"],
                    result=tc["result"],
                )
                for tc in tool_calls_made
            ]

        return ChatResponse(
            message=response_text,
            conversation_id=conversation.id,
            tool_calls=formatted_tool_calls,
        )

    except Exception as e:
        logger.error(f"Chat error for user {user_id}: {e}", exc_info=True)

        # Save error message to conversation
        error_message = "I'm having trouble connecting. Please try again."
        conv_repo.add_message(conversation.id, "assistant", error_message)

        return ChatResponse(
            message=error_message,
            conversation_id=conversation.id,
            tool_calls=None,
        )


@router.get("/conversations", response_model=List[ConversationSummary])
async def list_conversations(
    session: SessionDep,
    current_user: CurrentUserDep,
    limit: int = 20,
):
    """List user's recent conversations."""
    user_id = current_user.id

    if limit < 1 or limit > 100:
        limit = 20

    conv_repo = ConversationRepository(session)
    conversations = conv_repo.get_all_by_user(user_id, limit=limit)

    return [
        ConversationSummary(
            id=conv.id,
            title=conv.title,
            updated_at=conv.updated_at,
            message_count=conv_repo.get_message_count(conv.id),
        )
        for conv in conversations
    ]


@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(
    conversation_id: int,
    session: SessionDep,
    current_user: CurrentUserDep,
    message_limit: int = 50,
):
    """Get a conversation with its messages."""
    user_id = current_user.id

    if message_limit < 1 or message_limit > 100:
        message_limit = 50

    conv_repo = ConversationRepository(session)
    conversation = conv_repo.get_by_id_and_user(conversation_id, user_id)

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = conv_repo.get_messages(conversation_id, limit=message_limit)

    return ConversationDetail(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        messages=[
            MessageRead(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                tool_calls=msg.tool_calls,
                created_at=msg.created_at,
            )
            for msg in messages
        ],
    )


@router.delete("/conversations/{conversation_id}", status_code=204)
async def delete_conversation(
    conversation_id: int,
    session: SessionDep,
    current_user: CurrentUserDep,
):
    """Delete a conversation and all its messages."""
    user_id = current_user.id

    conv_repo = ConversationRepository(session)
    deleted = conv_repo.delete(conversation_id, user_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")

    logger.info(f"Deleted conversation {conversation_id} for user {user_id}")
