# MeetingRecorder: AI-Powered Meeting Recorder & Summarizer

# Overview

MeetingRecorder is a Windows desktop application designed to streamline virtual meetings by providing audio recording, transcription, and summarization. Built as a passion-driven side project, this tool leverages advanced speech-to-text and natural language processing (NLP) technologies to capture discussions, transcribe them with accuracy, and generate summaries. This project was developed to explore AI integration and enhance my skills in desktop application development and AI-driven solutions.

# Features

Audio Recording: Captures meeting audio seamlessly with minimal resource usage.

Speech-to-Text Transcription: Converts spoken content into text, handling diverse accents and noisy environments.

AI-Driven Summarization: Generates summaries using NLP

User-Friendly Interface: Simple, intuitive design for professionals to manage meeting outputs effortlessly.

Offline Capability: Processes recordings and transcriptions locally for privacy.

# Motivation
I built MeetingRecorder to challenge myself with cutting-edge AI technologies. The goal was to create a practical tool that addresses the chaos of virtual meetings while deepening my expertise in system architecture, audio processing, and AI model optimization. This is not a commercial product but a learning exercise to push the boundaries of AI-driven productivity tools.

# Technical Details

Platform: Windows (developed and tested on Windows 10/11), Unix(Tested in WSL Ubuntu) and hopefully Mac

Technologies: 

Speech-to-Text: Leverages pre-trained AI models for transcription (Whisper).

Summarization: Leverages built on transformer-based architectures(facebook/bart-large-cnn).

Frontend: PyQt.

# Installation
This project is a prototype and not distributed for public use. However, to run it locally:

Clone the repository.

Ensure dependencies are installed (requirements.txt).

run main.py

In the setting tab, provide the Hugging face token

# Usage
Launch MeetingRecorder.

Start a new meeting session and enable audio recording.

Select the recorded meeting (.wav file) and click transcribe.

After the meeting, generate a summary with one click, saved as a text file or displayed on-screen.

Review, edit, or export transcripts and summaries as needed.

# Limitations

Currently optimized for English-language meetings; multi-language support is experimental.

Performance may vary based on hardware and background noise levels.

Summarization accuracy depends on the complexity of discussions and model fine-tuning.

# Future Improvements

Add multi-language transcription support.

Enhance summarization with topic clustering for longer meetings.

Implement cloud-based processing for scalability (if commercialized and Enterprize edition).

Integrate with calendar tools for automated meeting context.

# Contributing
This is a personal side project, so contributions are not currently accepted. However, I’m open to feedback and ideas! Feel free to reach out via LinkedIn to discuss AI-driven tools, transcription challenges, or related projects.

# Disclaimer
MeetingRecorder is a non-commercial prototype built for skill development. It is not intended for production use or distribution. Ensure compliance with local laws regarding audio recording and data privacy when using similar tools.

# Contact
For questions, feedback, or collaboration ideas, connect with me on LinkedIn. Let’s talk AI, software engineering, or productivity tools!
