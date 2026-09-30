import os, html, requests, streamlit as st
from dotenv import load_dotenv
load_dotenv()
from backend.document_utils import format_docx, format_pdf

BACKEND_URL=os.getenv("BACKEND_URL","http://127.0.0.1:8000")
st.set_page_config(page_title="LegalEase",page_icon="⚖️",layout="wide")
st.title("⚖️ LegalEase")
st.caption("AI-Powered Legal Document Generator")
st.info("Generate, edit, preview and export draft legal documents.")

with st.form("legal_form"):
    document_type=st.text_input("Document Type","Freelance Work Contract")
    parties=st.text_area("Parties Involved","Jane Doe (Service Provider), TechNova Inc. (Client)")
    terms=st.text_area("Terms & Conditions","Payment to be made within 30 days of invoice; The provider agrees to deliver work by the agreed deadline; Confidentiality must be maintained at all times; Either party may terminate with 15 days notice")
    dates=st.text_input("Effective Date","April 15, 2025")
    submitted=st.form_submit_button("Generate Document",use_container_width=True)

if submitted:
    try:
        with st.spinner("Generating document with Gemini..."):
            r=requests.post(f"{BACKEND_URL}/generate",json={"document_type":document_type,"parties":parties,"terms":terms,"dates":dates},timeout=120)
        if r.ok:
            st.session_state["document"]=r.json()["document"]; st.session_state["doc_type"]=document_type
        else: st.error(r.json().get("detail",r.text))
    except requests.RequestException as e:
        st.error(f"Cannot connect to FastAPI backend: {e}")

if "document" in st.session_state:
    st.subheader("Generated Document")
    edited=st.text_area("Click to Edit Document",st.session_state["document"],height=500)
    st.session_state["document"]=edited
    st.subheader("Preview")
    st.markdown(f"<div style='padding:20px;border-radius:12px;background:#111827;color:#f3f4f6;white-space:pre-wrap'>{html.escape(edited)}</div>",unsafe_allow_html=True)
    a,b,c=st.columns(3)
    with a: st.download_button("Download TXT",edited.encode(),"legalease_document.txt","text/plain",use_container_width=True)
    with b: st.download_button("Download DOCX",format_docx(edited,st.session_state["doc_type"]),"legalease_document.docx","application/vnd.openxmlformats-officedocument.wordprocessingml.document",use_container_width=True)
    with c: st.download_button("Download PDF",format_pdf(edited,st.session_state["doc_type"]),"legalease_document.pdf","application/pdf",use_container_width=True)

st.divider()
st.caption("Draft only: have important legal documents reviewed by a qualified legal professional.")
