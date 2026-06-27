import streamlit as st
import tempfile

from parsers.pdf_parser import extract_pdf_text
from rag.chunker import chunk_pdf
from rag.embeddings import create_vector_store
from rag.retriever import search
from rag.llm import ask_llm
from services.web_search import search_web
from rag.context_checker import needs_web_search
from services.answer import get_answer_settings
from services.summary import generate_summary

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="PaperTutorAI",
    page_icon="📚",
    layout="wide"
)

# ----------------------------
# Session State
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_summary" not in st.session_state:
    st.session_state.show_summary = False

# All uploaded papers
if "papers" not in st.session_state:
    st.session_state.papers = []

# All chunks from every uploaded paper
if "all_chunks" not in st.session_state:
    st.session_state.all_chunks = []

if "knowledge_base_ready" not in st.session_state:
    st.session_state.knowledge_base_ready = False

if "selected_paper" not in st.session_state:
    st.session_state.selected_paper = None

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.title("📚 PaperTutorAI")

    st.markdown("---")

    uploaded_files = st.file_uploader(
        "Upload Research Papers",
        type=["pdf"],
        accept_multiple_files=True
    )

    uploaded_names = {
        p["filename"]
        for p in st.session_state.papers
    }

    new_files = []

    if uploaded_files:

        new_files = [
            f for f in uploaded_files
            if f.name not in uploaded_names
        ]

    if new_files:

        progress = st.progress(0, text="Processing papers...")

        papers = st.session_state.papers.copy()
        all_chunks = st.session_state.all_chunks.copy()

        total = len(new_files)

        for i, uploaded_file in enumerate(new_files):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as tmp:

                tmp.write(uploaded_file.read())
                temp_pdf = tmp.name

            pdf = extract_pdf_text(temp_pdf)

            chunks = chunk_pdf(pdf)

            papers.append({
                "filename": uploaded_file.name,
                "pages": pdf["num_pages"],
                "chunks": chunks
            })

            all_chunks.extend(chunks)

            progress.progress(
                int(((i + 1) / total) * 80),
                text=f"Processing {uploaded_file.name}"
            )

        progress.progress(
            90,
            text="Building knowledge base..."
        )

        create_vector_store(all_chunks)

        progress.progress(
            100,
            text="Done!"
        )

        progress.empty()

        st.session_state.papers = papers
        st.session_state.all_chunks = all_chunks
        st.session_state.knowledge_base_ready = True

        st.success(
            f"✅ Added {len(new_files)} paper(s).\n\n"
            f"Knowledge base now contains {len(papers)} paper(s)."
        )

    st.markdown("---")

    if st.session_state.papers:

        st.subheader("📚 Knowledge Base")

        paper_names = [
            paper["filename"]
            for paper in st.session_state.papers
        ]

        st.session_state.selected_paper = st.selectbox(
            "Select Paper",
            paper_names,
        )

        total_pages = sum(
            paper["pages"]
            for paper in st.session_state.papers
        )

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Papers",
                len(st.session_state.papers)
            )

        with col2:
            st.metric(
                "Pages",
                total_pages
            ) 

    if not st.session_state.papers:
        st.info("No papers uploaded yet.")

    st.subheader("Study Tools")

    if st.button(
        "📝 Generate Summary",
        use_container_width=True
    ):
        st.session_state.show_summary = True

    st.markdown("---")

    # Clear Chat Button
    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    if st.button("🗑 Clear Knowledge Base"):

        st.session_state.clear()

        import shutil
        import os

        if os.path.exists("vector_db"):
            shutil.rmtree("vector_db")

        os.makedirs("vector_db", exist_ok=True)

        st.rerun()

    st.markdown("---")

    answer_length = st.select_slider(
        "Answer Length",
        options=["Short", "Medium", "Detailed", "Very Detailed"],
        value="Detailed"
    )

# ----------------------------
# Main Page
# ----------------------------
st.title("📄 PaperTutorAI")

if "summary" in st.session_state:

    with st.expander(
        f"📝 Summary: {st.session_state.summary['paper']}",
        expanded=True,
    ):
        st.markdown(
            st.session_state.summary["text"]
        )

if (
    st.session_state.show_summary
    and st.session_state.all_chunks
):

    selected = next(
        paper
        for paper in st.session_state.papers
        if paper["filename"] == st.session_state.selected_paper
    )

    context = ""

    for chunk in selected["chunks"]:

        context += f"""
    ======================
    PAGE {chunk['page']}
    ======================

    {chunk['text']}
    """

    with st.spinner("Generating summary..."):

        summary = generate_summary(context)

    st.session_state.summary = {
        "paper": selected["filename"],
        "text": summary,
    }
    st.session_state.show_summary = False
    st.rerun()

# ----------------------------
# Display Chat History
# ----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------------------
# Chat Input
# ----------------------------
question = st.chat_input(
    "Ask something about your paper...",
    disabled=not st.session_state.knowledge_base_ready
)

if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    results = search(question)

    context = ""

    for chunk in results:

        context += f"""

        ########################################################

        Document: {chunk['source']}

        Page: {chunk['page']}

        ########################################################

        {chunk['text']}

        """

    web_context = ""

    # Questions that usually need background information
    keywords = [
        "what is",
        "define",
        "background",
        "overview",
        "meaning",
        "introduction"
    ]

    question_lower = question.lower()

    needs_background = any(
        keyword in question_lower
        for keyword in keywords
    )

    # Search the web only when needed
    if needs_background or needs_web_search(results):

        st.info("Searching the web for additional context...")

        websites = search_web(question)

        for site in websites[:3]:

            web_context += f"""
Title: {site['title']}

Summary: {site['body'][:250]}
"""
        context += f"""

    ====================================================
    EXTERNAL WEB REFERENCES
    ====================================================

    {web_context}
    """

    MAX_CONTEXT = 30000

    if len(context) > MAX_CONTEXT:
        context = context[:MAX_CONTEXT]

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
                settings = get_answer_settings(answer_length)

                answer = ask_llm(
                    question,
                    context,
                    settings,
                )

            except Exception as e:
                answer = f"❌ Error contacting the language model:\n\n{e}"

            answer += "\n\n---\n\n## Sources\n"

            seen = set()

            for chunk in results:

                key = (chunk["source"], chunk["page"])

                if key not in seen:

                    answer += (
                        f"- **{chunk['source']}** "
                        f"(Page {chunk['page']})\n"
                    )

                    seen.add(key)

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )