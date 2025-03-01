import streamlit as st
import json
import time
import random
import requests
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from ragEncyclopedia import RAGGale
from content_extraction import MedicalTranscriptProcessor
from Aud2Txt import Transcription

# API Key for Medical AI
GROQ_API_KEY = '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'
ragBook = RAGGale(GROQ_API_KEY)
meddoc = MedicalTranscriptProcessor(GROQ_API_KEY)

st.set_page_config(page_title="🩺 SurgiNote AI", page_icon="💊", layout="wide")

# UI Styling
st.markdown(
    """
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stButton>button {
            background: linear-gradient(to right, #56ab2f, #a8e063);
            color: white;
            font-weight: bold;
            border-radius: 10px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            transform: scale(1.1);
            background: linear-gradient(to right, #a8e063, #56ab2f);
        }
        .stDownloadButton>button {
            background: linear-gradient(to right, #ff416c, #ff4b2b);
            color: white;
            font-weight: bold;
            border-radius: 10px;
        }
        .stDownloadButton>button:hover {
            transform: scale(1.1);
            background: linear-gradient(to right, #ff4b2b, #ff416c);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.title("🩺 SurgiNote AI")
    st.image("https://c0.wallpaperflare.com/preview/648/982/424/adult-career-clipboard-doctor.jpg", caption="Healthcare AI", use_column_width=True)
    st.markdown("Transform medical transcripts into structured reports with AI insights.")
    
    uploaded_file = st.file_uploader("Upload Medical Transcript", type=["txt"])
    audio_button = st.button("🎙 Start Recording Audio")

    if audio_button:
        with st.spinner("Recording audio... Please wait"):
            time.sleep(random.randint(2, 5))
        st.success("Audio recorded successfully!")
        trans = Transcription()
        transcript = trans.real_time_transcription()
        result = meddoc.extract_medical_info(transcript)
        additional_info = ragBook.retrieve(transcript)
        st.session_state.processed_data = {
            "Structured Medical Information": result,
            "Additional Insights": additional_info
        }

# Main Content
st.image("https://via.placeholder.com/800x200", caption="AI-Powered Medical Documentation", use_column_width=True)
st.header("🔍 AI-Powered Medical Documentation")
st.markdown(
        """
        ### 🩺 SurgiNote AI - Medical Documentator
        SurgiNote AI is an advanced AI-powered medical documentation tool designed to streamline the process of extracting structured medical information from transcripts. Whether you're uploading a medical transcript file or using real-time speech-to-text transcription, SurgiNote AI efficiently processes the data, retrieves additional insights, and generates a professional medical report.

        ✨ **Key Features:** \n
        ✅ Real-time Speech Transcription – Convert spoken medical discussions into structured text.  
        ✅ Automated Medical Information Extraction – AI-powered extraction of key medical details.  
        ✅ Knowledge-Enhanced Insights – Retrieves additional relevant information from a medical database.  
        ✅ PDF Report Generation – Easily download structured medical documentation.  
        🚨 Emergency Notification System – If the phrase "notify emergency" is detected during transcription, the system automatically sends an emergency alert to a central server.  
        🛑 Voice-Controlled Transcription – Say "stop transcription" to end real-time transcription instantly.  

        Simply upload a transcript or record live audio, and let SurgiNote AI do the rest! 🚀
        """)    

if uploaded_file is not None:
    with st.spinner("Processing uploaded file..."):
        time.sleep(random.randint(2, 4))
    transcript = uploaded_file.read().decode("utf-8")
    result = meddoc.extract_medical_info(transcript)
    additional_info = ragBook.retrieve(transcript)
    st.session_state.processed_data = {
        "Structured Medical Information": result,
        "Additional Insights": additional_info
    }
    st.success("File processed successfully!")

if st.session_state.get("processed_data"):
    st.subheader("📑 Structured Medical Information")
    st.json(st.session_state.processed_data["Structured Medical Information"], expanded=True)
    st.subheader("📌 Additional Insights")
    st.json(st.session_state.processed_data["Additional Insights"], expanded=True)

    # Download Button
    def generate_pdf(data):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        elements.append(Paragraph("Medical Report", styles["Title"]))
        elements.append(Spacer(1, 12))
        elements.append(Image("https://via.placeholder.com/400x100"))
        elements.append(Spacer(1, 12))
        for section, content in data.items():
            elements.append(Paragraph(f"<b>{section}</b>", styles["Heading2"]))
            elements.append(Spacer(1, 6))
            if isinstance(content, dict):
                table_data = [[key, str(value)] for key, value in content.items()]
                table = Table(table_data, colWidths=[200, 300])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(table)
            else:
                elements.append(Paragraph(str(content), styles["BodyText"]))
            elements.append(Spacer(1, 12))
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()

    st.download_button(
        label="📥 Download Report as PDF",
        data=generate_pdf(st.session_state.processed_data),
        file_name="medical_document.pdf",
        mime="application/pdf"
    )
