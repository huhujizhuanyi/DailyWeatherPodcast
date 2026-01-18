# Daily Weather Podcast Generator

A local, automated workflow that generates a daily weather podcast using an AutoAgent framework with Small Language Models (SLMs) via Ollama, and converts the generated script into audio using the VibeVoice text-to-speech system.

## Overview

This project creates a fully automated pipeline for producing a daily weather podcast. The system autonomously generates a weather report script and converts it into a natural-sounding audio file, suitable for daily distribution through podcast platforms or personal listening.

## Architecture & Workflow

### 0. **Trigger AutoAgent Workflow to get local weather of current datetime**
   - Coordinates the entire process using an agent-based automation framework
   - Manages task sequencing, error handling, and data passing between components
   - Supports modular expansion for additional features (e.g., news integration, custom segments)

### 1. **Script Generation with SLM via Ollama in Workflow**
   - Uses Ollama to run a local Small Language Model (e.g., Llama 3, Mistral, Phi)
   - The model receives structured weather data and generates a natural, engaging podcast script
   - Prompt engineering ensures consistent format, tone, and inclusion of key weather details

### 2. **Text-to-Speech with VibeVoice**
   - Integrates [VibeVoice](https://github.com/vibevoice-community/VibeVoice.git) for high-quality audio synthesis
   - Converts the generated script into a spoken audio file
   - Supports voice customization, pacing adjustments, and emotional tone variations

### 3. **Output & Distribution**
   - Produces a final audio file (e.g., MP3, WAV)
   - Optionally adds intro/outro music or sound effects
   - Can be automated for daily publishing or stored locally

## Prerequisites

- **Ollama**: Installed and running locally with a suitable SLM pulled
- **Python 3.8+**: Core language for automation and integration
- **VibeVoice**: Cloned and set up from the official repository
- **ffmpeg**: For audio processing (if required by VibeVoice)

## Run

Run the main script:
```bash
bash run_vibe_voice.sh