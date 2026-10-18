# AI Video Assistant 🎥🤖

An intelligent AI-powered video and audio assistant application built with **Streamlit**, **Docker**, **Python**, **Whisper**, and **Sarvam AI**, designed to process, transcribe, and interact with video content seamlessly.

> **Status:** Fully functional in local development environments.

---

## 🌟 Key Features

* **Video & Audio Processing:** Download, extract, and handle media files efficiently using `yt-dlp`, `pydub`, and FFmpeg.
* **Speech-to-Text & Transcription:** High-accuracy audio transcription powered by OpenAI's Whisper models.
* **Localization & AI Integration:** Advanced processing capabilities integrated with Sarvam AI models.
* **Containerized Environment:** Fully dockerized setup ensuring consistent performance across platforms.
* **Interactive UI:** Clean web interface built using Streamlit.

---

## 🛠️ Tech Stack

* **Frontend / UI:** Streamlit
* **AI / ML Models:** OpenAI Whisper, Sarvam AI API
* **Media Processing:** `yt-dlp`, `pydub`, FFmpeg
* **Containerization:** Docker
* **Language:** Python

---

## 📁 Repository Structure

```text
AI-Video-Assitant/
├── app.py                 # Main Streamlit application entry point
├── audio_processor.py     # Core audio extraction and processing logic
├── requirements.txt       # Python package dependencies
├── Dockerfile             # Container configuration with FFmpeg & system dependencies
├── .env.example           # Environment variables template
└── README.md              # Project documentation
