# 🩺 SurgiNote AI - Medical Documentator

## Overview

SurgiNote AI is an intelligent medical documentation tool that transcribes, extracts, and structures medical information from audio or text inputs. It utilizes speech-to-text, AI-powered content extraction, and a Retrieval-Augmented Generation (RAG) system to enhance documentation quality.

---

## Features

- 🎤 **Real-Time Audio Transcription**
- 📄 **Text-Based Medical Transcript Processing**
- 🏥 **AI-Powered Medical Information Extraction**
- 🔍 **Contextual Insights Using RAG (Retrieval-Augmented Generation)**
- 📑 **PDF Report Generation**
- ⚠️ **Emergency Notification System**

---
## Tech Stack

**Speech Recognition**: Azure Cognitive Services Speech SDK

**Content Extraction**: GROQ

**Vector Search (RAG)**: Pinecone (Cloud), LangChain

**UI**: HTML, CSS, Streamlit

**Emergency Notification**: Socket

**PDF Download**: ReportLab

---

## Installation

### Prerequisites

- Python 3.8+
- API keys for Pinecone, Groq, and Azure Speech-to-Text

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/surginote-ai.git
   cd surginote-ai
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up API keys in the corresponding files:
   - `ragEncyclopedia.py` (Pinecone & Groq API keys)
   - `Aud2Txt.py` (Azure Speech API key)
4. Run the application:
   ```bash
   streamlit run app.py
   ```

---

## Usage

### 1️⃣ Upload a Transcript or Record Audio

- **Option 1**: Upload a `.txt` file containing a medical transcript.
- **Option 2**: Click the "Start Recording Audio" button to transcribe in real-time.

🖼️ *Insert image of the UI showing file upload and audio recording button*

### 2️⃣ AI Processing & Insights

- Extracts structured medical information.
- Retrieves additional insights using RAG (LLM-powered).

🖼️ *Insert image showing extracted medical data and AI insights*

### 3️⃣ Download PDF Report

- Once processed, download a structured report in PDF format.

🖼️ *Insert image showing the download button and sample PDF report*

---

## File Structure

```
📂 surginote-ai
│── app.py                   # Main application (Streamlit UI)
│── ragEncyclopedia.py       # RAG-based AI retrieval
│── notify_emergency.py      # Emergency alert system
│── content_extraction.py    # AI-based transcript processing
│── Aud2Txt.py               # Real-time speech-to-text conversion
│── requirements.txt         # Dependencies
│── README.md                # Documentation
```

---

## Future Improvements

- Integration with Electronic Health Records (EHR) systems
- Multilingual support for transcription
- Advanced medical reasoning using larger models

---

## Contributors

- **Jagaadhep U K**
- **KAVINKUMAR VS**
- **Rakshan A**
- **Mani Shankar S G** 

---

## Contact

For questions, reach out to [**ukjag2000@gmail.com**](mailto\:ukjag2000@gmail.com).

