from app.schemas.chat import ChatRequest


def test_chat_request_schema():
    payload = ChatRequest(message="Hello")

    assert payload.message == "Hello"