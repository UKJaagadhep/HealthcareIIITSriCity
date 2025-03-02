import streamlit as st
import json
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from ragEncyclopedia import RAGGale
from content_extraction import MedicalTranscriptProcessor
from Aud2Txt import Transcription

GROQ_API_KEY = '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'

ragBook = RAGGale(GROQ_API_KEY)
meddoc = MedicalTranscriptProcessor(GROQ_API_KEY)

if "pdf_ready" not in st.session_state:
    st.session_state.pdf_ready = False
if "processed_data" not in st.session_state:
    st.session_state.processed_data = None
if "pdf_buffer" not in st.session_state:
    st.session_state.pdf_buffer = None
if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None

def process_transcript(transcript):
    if not transcript:
        return {'error': 'No transcript provided'}
    
    medical_info = meddoc.extract_medical_info(transcript)
    additional_info = ragBook.retrieve(transcript)
    
    return {
        'Structured Medical Information': medical_info,
        'Additional Insights': additional_info
    }

def format_text(text):
    return text.replace("*", "").replace("**", "").strip()

def generate_pdf(content):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["Normal"]
  
    elements.append(Paragraph("Medical Transcript Report", title_style))
    elements.append(Spacer(1, 12))

    for section, data in content.items():
        elements.append(Paragraph(section, heading_style))
        elements.append(Spacer(1, 6))

        if isinstance(data, dict):
            table_data = []
            for key, value in data.items():
                formatted_key = format_text(key).replace("_", " ").title()
                formatted_value = format_text(str(value))
                table_data.append([formatted_key, formatted_value])

            table = Table(table_data, colWidths=[200, 300])
            table.setStyle(TableStyle([ 
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("PADDING", (0, 0), (-1, -1), 5)
            ]))
            elements.append(table)
        else:
            paragraphs = [Paragraph(format_text(line), normal_style) for line in data.split("\n")]
            elements.extend(paragraphs)

        elements.append(Spacer(1, 12))

    doc.build(elements)
    buffer.seek(0)
    return buffer

st.set_page_config(page_title="🩺 SurgiNote AI - Medical Documentator", page_icon=":clipboard:", layout="wide")

st.markdown("""
    <style>
        body {
            color: white;
        }
        .sidebar .sidebar-content {
            color: white;
        }
        .sidebar .sidebar-content h1, .sidebar .sidebar-content h2, .sidebar .sidebar-content p {
            color: white;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stDownloadButton>button {
            background-color: #FF5733;
            color: white;
            font-weight: bold;
        }
        .stDownloadButton>button:hover {
            background-color: #ff704d;
        }
        .stTextInput>div>input {
            background-color: #E4F1FE;
        }
        .stMarkdown {
            color: white;
        }
        .stFileUploader>div>div {
            background-color: #E4F1FE;
        }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🩺 SurgiNote AI - Medical Documentator")
    st.markdown("Upload a medical transcript (txt) or record audio to create structured medical documents.")
    
    uploaded_file = st.file_uploader("Upload a text file containing the medical transcript", type=["txt"])
    audio_button = st.button("Start Recording Audio")
    
    if audio_button:
        trans = Transcription()
        transcript = trans.real_time_transcription()
        result = process_transcript(transcript)
        
        st.session_state.processed_data = {
            "Structured Medical Information": result['Structured Medical Information'],
            "Additional Insights": result['Additional Insights']
        }
        
        st.session_state.pdf_buffer = generate_pdf(st.session_state.processed_data)
        st.session_state.pdf_ready = True

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
    if uploaded_file.name != st.session_state.last_uploaded_file:
        st.session_state.processed_data = None
        st.session_state.pdf_ready = False
        st.session_state.pdf_buffer = None
        st.session_state.last_uploaded_file = uploaded_file.name  

        transcript = uploaded_file.read().decode("utf-8")
        result = process_transcript(transcript)

        st.session_state.processed_data = {
            "Structured Medical Information": result['Structured Medical Information'],
            "Additional Insights": result['Additional Insights']
        }

        st.session_state.pdf_buffer = generate_pdf(st.session_state.processed_data)
        st.session_state.pdf_ready = True

if st.session_state.processed_data:
    st.subheader("Structured Medical Information:")
    st.write(st.session_state.processed_data["Structured Medical Information"])

    st.subheader("Additional Insights:")
    st.write(st.session_state.processed_data["Additional Insights"])

if st.session_state.pdf_ready and st.session_state.pdf_buffer:
    st.download_button(
        label="Download Report as PDF",
        data=st.session_state.pdf_buffer,
        file_name="medical_document.pdf",
        mime="application/pdf"
    )
