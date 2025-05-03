# 🎥 YouTube Downloader with FFmpeg Audio Conversion

This is a Python-based YouTube video/audio downloader using [yt-dlp](https://github.com/yt-dlp/yt-dlp). It allows users to:

- Download YouTube videos in MP4 format at a selected resolution
- Convert audio from Opus to AAC for better compatibility
- Download MP3 audio directly

---

## ⚙️ Features

- User-selectable video resolution
- Optional audio language selection
- Converts video audio to AAC using FFmpeg
- Safe, sanitized filenames for your OS
- Supports both `.mp4` and `.mp3` downloads

---

## 📦 Requirements

- Python 3.7+
- `yt-dlp` (installed via pip)
- `ffmpeg.exe` and `ffprobe.exe` (Windows) or FFmpeg installed on system (Linux/macOS)

---

## 📁 Setup Instructions

### 1. Clone this repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name


### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up FFmpeg

#### 🔹 For Windows:

1. Download FFmpeg static build from:
   👉 [https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip)

2. Extract and copy:

   * `ffmpeg.exe`
   * `ffprobe.exe`
     into a folder named `ffmpeg` inside the project directory:

```
project/
├── downloader.py
├── ffmpeg/
│   ├── ffmpeg.exe
│   └── ffprobe.exe
```

#### 🔹 For Linux/macOS:

Install FFmpeg globally:

```bash
sudo apt install ffmpeg  # Debian/Ubuntu
brew install ffmpeg      # macOS with Homebrew
```

Then adjust the script to use system ffmpeg path if needed.

---

## 🚀 How to Use

```bash
python downloader.py
```

* Paste the YouTube video URL when prompted.
* Choose whether you want an MP3 or MP4.
* Select video quality (for MP4).
* Select audio language (optional).
* Final file is saved in the current directory.

---

## 📝 Notes

* Output MP4 files are automatically converted to use **AAC audio** for maximum compatibility.
* Final video is saved as `YourVideoTitle_converted.mp4`.

---
