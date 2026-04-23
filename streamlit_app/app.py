import requests
import streamlit as st

API_URL = "http://backend:8000/api/v1"

st.set_page_config(
    page_title="KnowledgePilot AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 KnowledgePilot AI")
st.caption("GenAI Challenge Project - Chat + RAG Assistant")

tab1, tab2 = st.tabs(["💬 Chat", "📚 RAG Q&A"])

# -----------------------
# CHAT TAB
# -----------------------
with tab1:
    st.subheader("Talk with Base LLM")

    user_message = st.text_area(
        "Your message",
        height=150,
        key="chat_input"
    )

    if st.button("Send to Chat"):
        if user_message.strip():
            with st.spinner("Thinking..."):
                response = requests.post(
                    f"{API_URL}/chat",
                    json={"message": user_message},
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()

                    st.success("Response received")
                    st.markdown("### Reply")
                    st.write(data["reply"])

                    st.caption(
                        f'Model: {data["meta"]["model"]} | '
                        f'Latency: {data["meta"]["latency_ms"]} ms'
                    )
                else:
                    st.error(response.text)

# -----------------------
# RAG TAB
# -----------------------
with tab2:
    st.subheader("Ask Company Knowledge Base")

    rag_query = st.text_area(
        "Your question",
        height=150,
        key="rag_input"
    )

    top_k = st.slider("Top K Sources", 1, 5, 3)

    if st.button("Search Knowledge Base"):
        if rag_query.strip():
            with st.spinner("Searching and generating answer..."):
                response = requests.post(
                    f"{API_URL}/rag-query",
                    json={
                        "query": rag_query,
                        "top_k": top_k
                    },
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()

                    st.success("Answer generated")

                    st.markdown("### Answer")
                    st.write(data["answer"])

                    st.markdown("### Sources")

                    for source in data["sources"]:
                        st.info(
                            f'Source: {source["source"]} '
                            f'| Chunk: {source["chunk_id"]}'
                        )
                else:
                    st.error(response.text)