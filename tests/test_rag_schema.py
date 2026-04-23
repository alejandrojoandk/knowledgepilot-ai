from app.schemas.rag import RagRequest


def test_rag_request_schema():
    payload = RagRequest(query="Vacation days")

    assert payload.top_k == 3