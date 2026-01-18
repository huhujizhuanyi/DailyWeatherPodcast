#!/bin/bash

# VibeVoice Audio Generation Script
# This script clones VibeVoice, installs dependencies, and generates audio from podcast text

set -e  # Exit on error

echo "Step 1: Cloning VibeVoice repository..."
if [ ! -d "VibeVoice" ]; then
    git clone https://github.com/vibevoice-community/VibeVoice.git
else
    echo "VibeVoice directory already exists, skipping clone."
fi

echo "Step 2: Installing dependencies..."
cd VibeVoice/
uv pip install -e .

echo "Step 3: Generating podcast script..."
python podcast_app.py

echo "Step 4: Generating audio from podcast text..."
python demo/inference_from_file.py --txt_path ../podcast.txt --speaker_names Xinran Anchen

echo "Audio generation complete!"
