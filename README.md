# ASCII MV

A tool that converts videos into ASCII art music videos.

## Features

* Convert video frames into ASCII art
* Preserve the original video structure
* Render ASCII frames back into video
* Preserve original audio
* Support common video formats through FFmpeg

## Requirements

* Python 3.9+
* OpenCV
* NumPy
* Pillow
* FFmpeg

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd ascii-mv
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

**macOS**

```bash
brew install ffmpeg
```

**Ubuntu / Debian**

```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows**

```powershell
winget install Gyan.FFmpeg
```

## Usage

Place your input video in the `examples/` directory.

Then run:

```bash
python main.py
```

The generated ASCII music video will be saved to:

```text
output/ascii_mv.mp4
```

## Project Structure

```text
ascii-mv/
├── README.md
├── requirements.txt
├── main.py
├── converter.py
├── viewer.py
├── examples/
│   └── bad_apple.mp4
└── output/
```

## License

MIT License
