import streamlit as st
import pandas as pd
import sys
import os
sys.path.insert(0, "E:\\Clinical AI Copilot")

from components.tables import render_dark_table
from utils.state import initialize_state
from services.upload_service import upload_patient_dataset

st.set_page_config(page_title="Knowledge Base", page_icon="📚", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(180deg, #020817 0%, #030b1f 40%, #020617 100%); color: #f8fafc; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1400px; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #041127 0%, #020817 100%); border-right: 1px solid rgba(255,255,255,0.06); }
[data-testid="stSidebar"] * { color: #e5e7eb !important; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
div[data-testid="stVerticalBlock"] div:has(> div[data-testid="stMarkdownContainer"]) { background: transparent; }
.page-title { font-size: 2.2rem; font-weight: 800; color: #ffffff; margin-bottom: 0.35rem; }
.page-subtitle { color: #cbd5e1; font-size: 1rem; line-height: 1.75; margin-bottom: 1rem; }
.hero-card { background: linear-gradient(135deg, rgba(10,18,40,0.96), rgba(6,10,24,0.92)); border: 1px solid rgba(124,58,237,0.18); border-radius: 28px; padding: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.35); margin-bottom: 1.4rem; }
.pill { display: inline-block; padding: 0.6rem 1rem; border-radius: 999px; background: rgba(124,58,237,0.14); border: 1px solid rgba(124,58,237,0.35); color: #ddd6fe; font-size: 0.92rem; font-weight: 600; margin-bottom: 1rem; }
.info-box { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 1rem 1.1rem; color: #dbe4ff; margin-top: 1rem; line-height: 1.8; }
.kb-card { background: linear-gradient(180deg, rgba(8,15,32,0.95), rgba(4,9,20,0.95)); border: 1px solid rgba(255,255,255,0.06); border-radius: 18px; padding: 1.2rem; margin-bottom: 1rem; }
div.stButton > button { background: linear-gradient(90deg, #7c3aed, #2563eb); color: white; border: none; border-radius: 14px; padding: 0.85rem 1.3rem; font-weight: 700; font-size: 0.95rem; height: auto; width: 100%; }
div.stButton > button:hover { filter: brightness(1.06); }
[data-testid="stSuccess"] { background: rgba(16,185,129,0.14) !important; color: #d1fae5 !important; border: 1px solid rgba(16,185,129,0.28) !important; border-radius: 14px !important; }
[data-testid="stInfo"] { background: rgba(59,130,246,0.12) !important; color: #dbeafe !important; border: 1px solid rgba(59,130,246,0.22) !important; border-radius: 14px !important; }
[data-testid="stError"] { background: rgba(239,68,68,0.12) !important; color: #fee2e2 !important; border: 1px solid rgba(239,68,68,0.24) !important; border-radius: 14px !important; }

/* Labels white */
label, label p, .stTextInput label, .stTextInput label p,
.stFileUploader label, .stFileUploader label p,
[data-testid="stWidgetLabel"] p {
    color: #e2e8f0 !important;
    -webkit-text-fill-color: #e2e8f0 !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}

/* Button text white */
div.stButton > button, div.stButton > button p,
div.stButton > button span {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Input fields */
input[type="text"] {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    background: rgba(255,255,255,0.95) !important;
}

/* File uploader text */
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] span,
small {
    color: #cbd5e1 !important;
    -webkit-text-fill-color: #cbd5e1 !important;
}
</style>
""", unsafe_allow_html=True)

initialize_state()

st.markdown("""
<div class="hero-card">
    <div class="pill">Powered by Clinical AI + Multi-File RAG + Human Review</div>
    <div class="page-title">Knowledge Base</div>
    <div class="page-subtitle">
        Upload patient datasets and medical knowledge documents to power the AI agent.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📂 Upload Patient Data",
    "📖 Upload Medical Knowledge",
    "🔍 Search Knowledge Base"
])


# ── Tab 1: Patient Data Upload ─────────────────────────────────────────────────
with tab1:
    st.markdown("### Upload Patient Dataset")
    st.markdown("Upload a CSV file containing patient records. The system will automatically detect columns.")

    uploaded_file = st.file_uploader(
    "Upload patient dataset (CSV, Excel, TXT)",
    type=["csv", "xlsx", "xls", "txt"],
    accept_multiple_files=False,
    key="patient_upload",
    help="Supports CSV, Excel (.xlsx), and TXT files. Columns like name, age, gender will be auto-detected.",
)

    if uploaded_file is not None:
        rows = [{"file_name": uploaded_file.name, "size": f"{len(uploaded_file.getvalue())/1024:.1f} KB", "type": uploaded_file.type or "text/csv"}]
        render_dark_table("Selected File", pd.DataFrame(rows))

        if st.button("Process Upload", key="process_upload_btn"):
            try:
                with st.spinner("Uploading and processing dataset..."):
                    result = upload_patient_dataset(uploaded_file, filename=uploaded_file.name)

                st.session_state["last_upload_result"] = result
                st.session_state["upload_done"] = True
                st.success("✅ Dataset uploaded and processed successfully.")

                st.markdown(
                    f"""
                    <div class="info-box">
                        <b>Filename:</b> {result.get("filename", "-")}<br>
                        <b>Patients Created:</b> {result.get("patients_created", 0)}<br>
                        <b>Message:</b> {result.get("message", "-")}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            except Exception as e:
                st.error(f"Upload failed: {str(e)}")
    else:
        st.info("Choose a CSV file to begin.")

    if st.session_state.get("upload_done"):
        if st.button("Go to Patients Page", key="goto_patients_btn"):
            st.switch_page("pages/1_Patients.py")


# ── Tab 2: Medical Knowledge Upload ───────────────────────────────────────────
with tab2:
    st.markdown("### Upload Medical Knowledge")
    st.markdown("Upload clinical guidelines, research papers, or medical protocols. The AI agent will search these when answering questions.")

    kb_file = st.file_uploader(
        "Upload medical document",
        type=["txt", "csv"],
        accept_multiple_files=False,
        key="kb_upload",
        help="Upload TXT or CSV files containing medical guidelines, protocols, or reference data.",
    )

    doc_title = st.text_input("Document Title", placeholder="e.g. Clinical Guidelines for Diabetes Management")
    doc_source = st.text_input("Source", placeholder="e.g. WHO Guidelines 2024")

    if kb_file is not None and st.button("Add to Knowledge Base", key="kb_upload_btn"):
        if not doc_title:
            st.warning("Please enter a document title.")
        else:
            try:
                with st.spinner("Processing and indexing document..."):
                    content = kb_file.read().decode("utf-8-sig", errors="ignore")

                    # Chunk and store in Qdrant
                    from ai_engine.embeddings.qdrant_service import store_document_chunks, chunk_text

                    chunks_text = chunk_text(content, chunk_size=300, overlap=50)
                    chunks = [
                        {
                            "text": chunk,
                            "source": doc_source or kb_file.name,
                            "section_title": doc_title,
                            "document_id": kb_file.name,
                        }
                        for chunk in chunks_text
                    ]

                    stored = store_document_chunks(chunks)

                st.success(f"✅ Document indexed successfully! {stored} chunks stored in Qdrant.")
                st.markdown(
                    f"""
                    <div class="info-box">
                        <b>Title:</b> {doc_title}<br>
                        <b>Source:</b> {doc_source or kb_file.name}<br>
                        <b>Chunks stored:</b> {stored}<br>
                        <b>Status:</b> Ready for AI agent search
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            except Exception as e:
                st.error(f"Failed to index document: {str(e)}")
    elif kb_file is None:
        st.info("Upload a TXT or CSV file containing medical knowledge.")

    # Show sample knowledge types
    st.markdown("---")
    st.markdown("**Recommended document types:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="kb-card">
            <div style="font-size:1.5rem;">📋</div>
            <div style="color:#f5f7ff; font-weight:700; margin: 0.5rem 0;">Clinical Guidelines</div>
            <div style="color:#9ca3c9; font-size:0.9rem;">Treatment protocols, diagnostic criteria, reference ranges</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="kb-card">
            <div style="font-size:1.5rem;">💊</div>
            <div style="color:#f5f7ff; font-weight:700; margin: 0.5rem 0;">Drug Information</div>
            <div style="color:#9ca3c9; font-size:0.9rem;">Drug interactions, dosing guidelines, contraindications</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="kb-card">
            <div style="font-size:1.5rem;">🔬</div>
            <div style="color:#f5f7ff; font-weight:700; margin: 0.5rem 0;">Lab References</div>
            <div style="color:#9ca3c9; font-size:0.9rem;">Normal ranges, critical values, interpretation guides</div>
        </div>
        """, unsafe_allow_html=True)


# ── Tab 3: Search Knowledge Base ───────────────────────────────────────────────
with tab3:
    st.markdown("### Search Knowledge Base")
    st.markdown("Test what the AI agent will find when answering clinical questions.")

    search_query = st.text_input(
        "Search query",
        placeholder="e.g. elevated creatinine kidney disease treatment",
        key="kb_search"
    )

    if st.button("Search", key="kb_search_btn"):
        if not search_query.strip():
            st.warning("Please enter a search query.")
        else:
            try:
                with st.spinner("Searching knowledge base..."):
                    from ai_engine.embeddings.qdrant_service import search_similar
                    results = search_similar(search_query, top_k=5)

                if results:
                    st.success(f"Found {len(results)} relevant chunks")
                    for i, result in enumerate(results, 1):
                        st.markdown(
                            f"""
                            <div class="kb-card">
                                <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
                                    <div style="color:#a78bfa; font-weight:700;">Result {i} — {result.get('source', 'Unknown')}</div>
                                    <div style="color:#10b981; font-size:0.85rem;">Relevance: {result.get('score', 0):.2f}</div>
                                </div>
                                <div style="color:#9ca3c9; font-size:0.85rem; margin-bottom:0.5rem;">{result.get('section_title', '')}</div>
                                <div style="color:#e2e8f0; font-size:0.9rem; line-height:1.6;">{result.get('text', '')[:400]}...</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                else:
                    st.info("No results found. Upload medical documents to populate the knowledge base.")

            except Exception as e:
                st.error(f"Search failed: {str(e)}")

    