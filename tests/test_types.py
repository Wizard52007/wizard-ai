from datetime import timezone
from uuid import UUID
from wizard.core.types import (
    ExecutionContext,
    Message,
    MessageRole,
    Request,
    Response,
    ToolRequest,
    ToolResult,
)

def test_message_creation():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    assert message.role == MessageRole.USER
    assert message.content == "Hello Wizard"


def test_message_timestamp_is_utc():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    assert message.timestamp.tzinfo == timezone.utc


def test_message_roles():
    assert MessageRole.SYSTEM.value == "system"
    assert MessageRole.USER.value == "user"
    assert MessageRole.ASSISTANT.value == "assistant"
    assert MessageRole.TOOL.value == "tool"


def test_request_creation():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)

    assert request.message == message
    assert isinstance(request.request_id, UUID)


def test_request_timestamp_is_utc():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)

    assert request.timestamp.tzinfo == timezone.utc


def test_requests_have_unique_ids():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request_one = Request.create(message)
    request_two = Request.create(message)

    assert request_one.request_id != request_two.request_id


def test_response_creation():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)

    response = Response.create(
        request.request_id,
        "Hello! How can I help?",
    )

    assert response.request_id == request.request_id
    assert response.content == "Hello! How can I help?"


def test_response_timestamp_is_utc():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)

    response = Response.create(
        request.request_id,
        "Hello!",
    )

    assert response.timestamp.tzinfo == timezone.utc


def test_response_links_to_request():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)

    response = Response.create(
        request.request_id,
        "Hello!",
    )

    assert response.request_id == request.request_id


def test_tool_request_creation():
    message = Message.create(
        MessageRole.USER,
        "Open Chrome",
    )

    request = Request.create(message)

    arguments = {
        "url": "https://google.com",
    }

    tool_request = ToolRequest.create(
        request.request_id,
        "open_browser",
        arguments,
    )

    assert tool_request.request_id == request.request_id
    assert tool_request.tool_name == "open_browser"
    assert tool_request.arguments == arguments


def test_tool_request_timestamp_is_utc():
    message = Message.create(
        MessageRole.USER,
        "Open Chrome",
    )

    request = Request.create(message)

    tool_request = ToolRequest.create(
        request.request_id,
        "open_browser",
        {},
    )

    assert tool_request.timestamp.tzinfo == timezone.utc


def test_tool_request_preserves_arguments():
    message = Message.create(
        MessageRole.USER,
        "Search for VJTI",
    )

    request = Request.create(message)

    arguments = {
        "query": "VJTI Mumbai",
        "new_tab": True,
    }

    tool_request = ToolRequest.create(
        request.request_id,
        "search_web",
        arguments,
    )

    assert tool_request.arguments["query"] == "VJTI Mumbai"
    assert tool_request.arguments["new_tab"] is True


def test_tool_result_success():
    message = Message.create(
        MessageRole.USER,
        "Search for VJTI",
    )

    request = Request.create(message)

    data = {
        "results": ["VJTI Mumbai"],
    }

    result = ToolResult.create(
        request.request_id,
        success=True,
        data=data,
    )

    assert result.request_id == request.request_id
    assert result.success is True
    assert result.data == data
    assert result.error is None


def test_tool_result_failure():
    message = Message.create(
        MessageRole.USER,
        "Open Chrome",
    )

    request = Request.create(message)

    result = ToolResult.create(
        request.request_id,
        success=False,
        error="Chrome is not installed",
    )

    assert result.request_id == request.request_id
    assert result.success is False
    assert result.data is None
    assert result.error == "Chrome is not installed"


def test_tool_result_timestamp_is_utc():
    message = Message.create(
        MessageRole.USER,
        "Run a tool",
    )

    request = Request.create(message)

    result = ToolResult.create(
        request.request_id,
        success=True,
        data="Done",
    )

    assert result.timestamp.tzinfo == timezone.utc


def test_tool_result_preserves_data():
    message = Message.create(
        MessageRole.USER,
        "Get system information",
    )

    request = Request.create(message)

    data = {
        "os": "Windows",
        "version": 11,
        "online": True,
    }

    result = ToolResult.create(
        request.request_id,
        success=True,
        data=data,
    )

    assert result.data["os"] == "Windows"
    assert result.data["version"] == 11
    assert result.data["online"] is True


def test_execution_context_creation():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)

    context = ExecutionContext.create(request)

    assert context.request == request
    assert context.messages == [message]
    assert context.tool_results == []


def test_execution_context_preserves_request():
    message = Message.create(
        MessageRole.USER,
        "Open Chrome",
    )

    request = Request.create(message)

    context = ExecutionContext.create(request)

    assert context.request.request_id == request.request_id
    assert context.request.message == message


def test_execution_context_starts_with_request_message():
    message = Message.create(
        MessageRole.USER,
        "Search for VJTI",
    )

    request = Request.create(message)

    context = ExecutionContext.create(request)

    assert len(context.messages) == 1
    assert context.messages[0] == request.message


def test_execution_context_starts_without_tool_results():
    message = Message.create(
        MessageRole.USER,
        "Run a tool",
    )

    request = Request.create(message)

    context = ExecutionContext.create(request)

    assert context.tool_results == []
