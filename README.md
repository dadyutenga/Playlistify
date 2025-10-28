# 🎥 Playlistify - YouTube Playlist Downloader (Enhanced)

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/patrick-paul/Playlistify)

> **Stop wasting time with broken tools and paid services.** Download entire YouTube playlists or single videos with one command - completely free, automatic, and blazing fast with parallel downloads.

## 😤 The Problem

You want to download a YouTube playlist. Simple, right? **Wrong.**

- 🚫 **Online tools** require subscriptions or have video limits
- 💸 **Paid software** charges $20-50 for basic functionality
- 🐌 **Slow downloads** take hours for large playlists
- 🐛 **Broken scripts** require manual ffmpeg installation, PATH configuration, and often fail silently
- ⏰ **Hours wasted** troubleshooting dependencies and cryptic error messages

**I spent 2 hours fighting with tools that don't work.** You shouldn't have to.

## ✨ The Solution

**Playlistify** is a Python script that:
- ✅ **Works immediately** - auto-installs all dependencies
- ✅ **100% free** - no subscriptions, no limits
- ✅ **Cross-platform** - Windows, macOS, Linux
- ✅ **Smart** - detects your OS and configures everything automatically
- ✅ **No manual setup** - installs yt-dlp, ffmpeg, and adds to PATH automatically
- ⚡ **Blazing fast** - parallel downloads (3x+ faster than sequential)
- 🎯 **Flexible** - single videos, playlists, ranges, or custom selections
- 🖥️ **Two interfaces** - CLI for power users, GUI for everyone else
- 🔄 **Reliable** - automatic retry on failures with progress tracking

## 🚀 Quick Start

### Prerequisites

**Only Python 3.7+ is required.** Everything else installs automatically.

**Don't have Python?** Download it here:
- **Windows**: [Python.org](https://www.python.org/downloads/) - ⚠️ **CHECK "Add Python to PATH" during installation**
- **macOS**: [Python.org](https://www.python.org/downloads/) or `brew install python3`
- **Linux**: Usually pre-installed. If not: `sudo apt install python3 python3-pip`

### Installation

1. **Clone or download this repository:**
   ```bash
   git clone https://github.com/patrick-paul/Playlistify.git
   cd Playlistify
   ```

2. **Run the script:**
   ```bash
   python playlist_downloader.py
   ```

That's it! The script will:
- ✓ Check for yt-dlp (auto-install if missing)
- ✓ Check for ffmpeg (auto-install if missing)
- ✓ Add ffmpeg to PATH (Windows)
- ✓ Show you a menu with options

## 🎮 Usage Guide

### First Run - Automatic Setup

When you run the script for the first time:

```bash
$ python playlist_downloader.py

==================================================
Checking dependencies...
==================================================

Detected OS: windows

[1/2] Checking yt-dlp...
  ✓ yt-dlp is already installed
  ✓ Updated to latest version

[2/2] Checking ffmpeg...
  ✗ ffmpeg not found
  Install ffmpeg now? (y/n): y
  
  Downloading ffmpeg manually...
  Downloading from https://www.gyan.dev/ffmpeg/builds/...
  Extracting...
  ✓ ffmpeg installed to C:\Users\YourName\ffmpeg
  ✓ Added to PATH

==================================================
Setup complete!
==================================================
```

**Important Notes:**
- On **Windows**, you may need to restart your terminal after first run for PATH changes to take effect
- On **macOS**, it will use Homebrew to install ffmpeg (install Homebrew first if needed)
- On **Linux**, it will use your package manager (apt/yum/dnf/pacman)

### Interface Selection

After setup, choose your preferred interface:

```
Select mode:
1. Command Line Interface (CLI)
2. Graphical User Interface (GUI)

Enter choice (1-2):
```

---

## 📖 Feature Guide

### 1️⃣ GUI Mode (Easiest)

Perfect for beginners or anyone who prefers a visual interface.

**To launch GUI:**
```bash
python playlist_downloader.py
# Choose option 2
```

**GUI Features:**
- 🔗 **URL Input** - Paste any YouTube video or playlist URL
- 🎬 **Type Selection** - Toggle between single video or playlist
- 🎨 **Quality Selector** - Dropdown menu with quality options
- ⚡ **Parallel Downloads** - Checkbox to enable with worker count slider
- 📊 **Video Range** - Select specific videos (e.g., 10-20)
- 📁 **Directory Browser** - Click to choose save location
- 📝 **Real-time Log** - See progress and status updates
- 🔄 **Progress Bar** - Visual download indicator

**GUI Screenshot Flow:**
1. Paste URL → `https://www.youtube.com/playlist?list=...`
2. Select type → `Playlist`
3. Choose quality → `1080p`
4. Enable parallel → ✓ `Workers: 3`
5. Click **Download** → Watch it work!

---

### 2️⃣ CLI Mode (Power Users)

For terminal lovers and automation scripts.

#### Option 1: Single Video Download

```bash
Enter YouTube URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ

✓ Single video detected

Available qualities:
  best   - Best available quality
  1080p  - Full HD
  720p   - HD
  480p   - SD
  worst  - Lowest quality (smallest file)

Enter quality (press Enter for 'best'): 1080p
Enter output directory (press Enter for 'downloads'): MyVideos

Video will be saved to: C:\Users\You\Playlistify\MyVideos
Downloading video (Attempt 1/3)...
[download] 100% of 45.2MiB in 00:23
✓ Download complete!
```

**Features:**
- ✅ Automatic quality selection
- ✅ Progress bar with speed and ETA
- ✅ Auto-retry up to 3 times on failure
- ✅ Clean filenames with spaces: `My Video Title.mp4`

---

#### Option 2: Playlist - List Videos Only

Preview what's in a playlist before downloading:

```bash
Enter YouTube URL: https://www.youtube.com/playlist?list=...

✓ Playlist detected

What would you like to do?
1. List all videos (no download)
2. Download entire playlist (sequential)
3. Download entire playlist (parallel - faster)
4. Download specific video range
5. Download with custom quality

Enter choice (1-5): 1

Fetching playlist information...

Found 47 videos in playlist:

--------------------------------------------------------------------------------
  1. Introduction to Python
     URL: https://www.youtube.com/watch?v=... | Duration: 15:30

  2. Variables and Data Types
     URL: https://www.youtube.com/watch?v=... | Duration: 22:45

  3. Control Flow - If Statements
     URL: https://www.youtube.com/watch?v=... | Duration: 18:12
...
```

---

#### Option 3: Sequential Download (Slower, Safer)

Good for unstable connections or when you don't want to hammer the server:

```bash
Enter choice (1-5): 2
Enter output directory (press Enter for 'downloads'): Python_Course

Videos will be saved to: C:\Users\You\Playlistify\Python_Course
Downloading playlist to: Python_Course
Quality: best
--------------------------------------------------
[download] Downloading item 1 of 47
[download] 001 - Introduction to Python.mp4 has already been downloaded
[download] Downloading item 2 of 47
[download] 15.3% of 89.2MiB at 2.4MiB/s ETA 00:31
```

**When to use sequential:**
- Slow/unstable internet connection
- Server rate limiting issues
- You want to monitor each download closely

---

#### Option 4: Parallel Download (3x+ Faster) ⚡

**This is the recommended method for most users!**

```bash
Enter choice (1-5): 3
Enter output directory (press Enter for 'downloads'): Python_Course
Number of parallel downloads (1-10, press Enter for 3): 5

Videos will be saved to: C:\Users\You\Playlistify\Python_Course
Using 5 parallel workers

Fetching playlist information...
Found 47 videos
Starting parallel download with 5 workers...
Output directory: C:\Users\You\Playlistify\Python_Course
--------------------------------------------------
✓ [001] Introduction to Python (1/47)
✓ [002] Variables and Data Types (2/47)
✓ [003] Control Flow - If Statements (3/47)
✓ [004] Functions and Modules (4/47)
✓ [005] Lists and Tuples (5/47)
...

==================================================
Download complete!
Successful: 47/47
==================================================
```

**Benefits:**
- ⚡ **3-5x faster** than sequential (depending on worker count)
- 🎯 Downloads 3-5 videos simultaneously by default
- 🔄 Automatic retry on each video (up to 3 attempts)
- 📊 Real-time progress tracking
- ✅ Continues even if some videos fail
- 📝 Summary report at the end

**Recommended worker counts:**
- **3 workers** - Safe default, works on most connections
- **5 workers** - Fast, good for stable broadband
- **8-10 workers** - Maximum speed, requires excellent connection
- **1 worker** - Same as sequential but with better error handling

---

#### Option 5: Download Video Range

Download only specific videos from a playlist (e.g., videos 15-30):

```bash
Enter choice (1-5): 4

Enter video range to download:
  Start from video number: 15
  End at video number: 30

Enter output directory (press Enter for 'downloads'): 
Use parallel downloads? (y/n, press Enter for yes): y
Number of parallel downloads (1-10, press Enter for 3): 5

Videos will be saved to: C:\Users\You\Playlistify\downloads
Downloading videos 15 to 30 (16 videos)
Starting parallel download with 5 workers...
--------------------------------------------------
✓ [015] Advanced Functions (1/16)
✓ [016] Decorators (2/16)
✓ [017] Generators (3/16)
...
```

**Use cases:**
- You only need a specific section of a course
- Resume after manual cancellation
- Download in chunks to manage disk space
- Skip intro/outro videos

---

#### Option 6: Custom Quality

Choose specific quality for all videos:

```bash
Enter choice (1-5): 5

Available qualities:
  best   - Best available quality
  1080p  - Full HD
  720p   - HD
  480p   - SD
  worst  - Lowest quality (smallest file)

Enter quality (press Enter for 'best'): 720p
Enter output directory (press Enter for 'downloads'): 
Use parallel downloads? (y/n, press Enter for yes): y
Number of parallel downloads (1-10, press Enter for 3): 

Videos will be saved to: C:\Users\You\Playlistify\downloads
Using 3 parallel workers
Starting parallel download...
```

**Quality guide:**
- `best` - Highest available (could be 4K, 1440p, or 1080p)
- `1080p` - Full HD (1920x1080) - **Recommended for most users**
- `720p` - HD (1280x720) - Good balance of quality and size
- `480p` - SD (854x480) - Small files, acceptable quality
- `worst` - Lowest available - Minimal disk space

**File sizes (approximate per hour):**
- 1080p: 1-2 GB/hour
- 720p: 500-800 MB/hour
- 480p: 200-400 MB/hour

---

## 🎯 Real-World Usage Examples

### Example 1: Download Entire Course
```bash
# Full programming course (100+ videos)
python playlist_downloader.py
# Choose: GUI mode OR CLI → Parallel download with 5 workers
# Result: ~2 hours for 100 videos vs ~8 hours sequential
```

### Example 2: Download Music Playlist
```bash
# Music videos in best quality
python playlist_downloader.py
# Choose: CLI → Custom quality → "best" → Parallel 3 workers
# Clean filenames: "Artist Name - Song Title.mp4"
```

### Example 3: Download Specific Lectures
```bash
# Only lectures 20-35 from a university course
python playlist_downloader.py
# Choose: CLI → Video range → 20 to 35 → Parallel download
# Only downloads 16 videos instead of 100+
```

### Example 4: Low Storage Situation
```bash
# Download in 480p to save space
python playlist_downloader.py
# Choose: CLI → Custom quality → "480p" → Parallel download
# 70% smaller files, still watchable
```

### Example 5: Unstable Connection
```bash
# Your internet drops frequently
python playlist_downloader.py
# Choose: CLI → Sequential download (option 2)
# Auto-retry ensures every video downloads eventually
```

---

## 🔧 Advanced Features

### Automatic Retry Logic

Every download attempt includes:
- **3 retry attempts** per video
- **3-second delay** between retries
- **Automatic resume** if script crashes (run again)
- **Error logging** for troubleshooting

### Smart File Naming

- **Single videos**: `Video Title with Spaces.mp4`
- **Playlists**: `001 - First Video.mp4`, `002 - Second Video.mp4`
- **No underscores** - Natural, readable filenames
- **Proper sorting** - Zero-padded numbers for correct order

### Progress Tracking

**Sequential downloads:**
```
[download] 34.5% of 156.2MiB at 3.2MiB/s ETA 00:42
```

**Parallel downloads:**
```
✓ [023] Advanced Python Techniques (23/50)
✓ [024] Object Oriented Programming (24/50)
✗ [025] Design Patterns - Connection timeout (will retry)
✓ [026] Testing and Debugging (25/50)
```

### Error Handling

The script handles:
- ❌ Network timeouts → Auto-retry
- ❌ YouTube rate limiting → Continues with other videos
- ❌ Corrupted downloads → Re-downloads
- ❌ Private/deleted videos → Skips and logs
- ❌ Age-restricted content → Downloads if possible

---

## 📁 Output Structure

### Default Structure
```
Playlistify/
├── playlist_downloader.py
└── downloads/
    ├── 001 - Introduction to Programming.mp4
    ├── 002 - Variables and Data Types.mp4
    ├── 003 - Control Flow Statements.mp4
    └── ...
```

### Custom Structure
```
Playlistify/
├── playlist_downloader.py
├── Python_Course/
│   ├── 001 - Intro.mp4
│   └── ...
├── Music_Videos/
│   ├── Artist - Song 1.mp4
│   └── ...
└── Documentaries/
    └── ...
```

---

## 🐛 Troubleshooting

### "Python is not recognized as a command"

**Windows:**
1. Reinstall Python from [Python.org](https://www.python.org/downloads/)
2. ✅ **CHECK the "Add Python to PATH" box during installation**
3. Restart your terminal/command prompt

**macOS/Linux:**
- Try `python3` instead of `python`
- Install Python: `brew install python3` (macOS) or `sudo apt install python3` (Linux)

---

### "ffmpeg installation failed"

**Manual installation:**

**Windows:**
1. Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg` to PATH:
   - Search "Environment Variables" in Start menu
   - Edit "Path" under "User variables"
   - Add new entry: `C:\ffmpeg`
   - Click OK and restart terminal

**macOS:**
```bash
# Install Homebrew first if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Then install ffmpeg
brew install ffmpeg
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

---

### "Videos download as separate .webm files"

**Problem:** ffmpeg is not installed or not in PATH

**Solution:**
1. Close the script
2. Run it again: `python playlist_downloader.py`
3. When asked "Install ffmpeg now?", type `y` and press Enter
4. **Windows users:** Restart your terminal after installation
5. Run the script again

---

### "WARNING: nsig extraction failed"

**This is NORMAL and can be ignored.** YouTube constantly changes their code to prevent downloads, but yt-dlp handles it automatically. Your videos will download successfully.

---

### "Rate limited by YouTube" / "HTTP Error 429"

YouTube is temporarily blocking your IP.

**Solutions:**
1. **Wait 1-2 hours** before trying again
2. **Use fewer parallel workers** (try 1-2 instead of 5)
3. **Use a VPN** to change your IP address
4. **Update yt-dlp**: `pip install --upgrade yt-dlp`
5. **Use sequential downloads** (slower but less aggressive)

---

### "Download stuck at 0%"

**Causes:**
- Video is private/deleted
- Age-restricted content
- Network connectivity issue

**Solutions:**
1. Press `Ctrl+C` to stop
2. Run the script again (it will skip completed videos)
3. Check if you can watch the video in a browser
4. Try with option "5" and select "worst" quality as a test

---

### Parallel download fails immediately

**Problem:** Too many workers for your connection

**Solution:**
- Reduce workers to 1-3
- Check your internet speed: [fast.com](https://fast.com)
- Try sequential download instead

---

### GUI doesn't open / tkinter error

**Linux users:**
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

**macOS/Windows:** tkinter should be included with Python

---

### Downloaded videos won't play

**Problem:** Incomplete download or missing codec

**Solutions:**
1. Delete the file
2. Run the script again (it will re-download)
3. Install VLC Media Player (plays everything)
4. Update ffmpeg: Re-run script and choose to install ffmpeg

---

### Script crashes mid-download

**Don't worry!** Just run it again:
```bash
python playlist_downloader.py
```

The script will:
- ✅ Skip already downloaded videos
- ✅ Continue where it left off
- ✅ Resume incomplete downloads

---

## 💡 Tips & Best Practices

### For Best Performance

1. **Use parallel downloads** (3-5 workers) for playlists
2. **Choose 1080p** unless you need 4K or want to save space
3. **Close other programs** using internet bandwidth
4. **Use wired connection** instead of WiFi when possible
5. **Don't download during peak hours** (YouTube may throttle)

### For Reliability

1. **Start with small playlists** (10-20 videos) to test
2. **Use sequential downloads** if your internet is unstable
3. **Download in chunks** using video range feature
4. **Keep yt-dlp updated** (script auto-updates on each run)

### For Organization

1. **Use descriptive folder names**: `Python_Course_2024` instead of `downloads`
2. **Separate by category**: Create different folders for different playlists
3. **Check quality before downloading entire playlist**: Download 1-2 videos first to verify

### Storage Management

```bash
# Check available space first
# Windows: Check "This PC" in File Explorer
# macOS/Linux: df -h

# Estimate space needed:
# 1080p: ~1.5 GB per hour of video
# 720p: ~700 MB per hour
# 480p: ~300 MB per hour

# Example: 50-video playlist, 20 min each
# Total time: ~16.5 hours
# Space needed (1080p): ~25 GB
# Space needed (720p): ~11 GB
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Issues

Found a bug? [Open an issue](https://github.com/patrick-paul/Playlistify/issues) with:
- Your operating system and Python version
- The full error message (copy from terminal)
- Steps to reproduce the problem
- The URL you tried to download (if not private)

### Suggesting Features

Have an idea? [Open an issue](https://github.com/patrick-paul/Playlistify/issues) with:
- Description of the feature
- Why it would be useful
- How it might work

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test on your platform
5. Update README if needed
6. Submit a pull request with clear description

### Completed Features ✅

- [x] ~~Add progress bar for individual video downloads~~ ✅ **DONE**
- [x] ~~Implement parallel downloads for faster speed~~ ✅ **DONE**
- [x] ~~Add GUI interface~~ ✅ **DONE**
- [x] ~~Download specific video ranges (e.g., videos 10-20)~~ ✅ **DONE**
- [x] ~~Automatic retry on failed downloads~~ ✅ **DONE**
- [x] ~~Single video download support~~ ✅ **DONE**

### Ideas for Future Contributions

- [ ] Add subtitle download support (SRT files)
- [ ] Support for other video platforms (Vimeo, Dailymotion)
- [ ] Filter by duration (e.g., only videos under 10 minutes)
- [ ] Export playlist metadata as JSON/CSV
- [ ] Support for member-only content (cookies authentication)
- [ ] Audio-only download mode (MP3 extraction)
- [ ] Thumbnail extraction
- [ ] Scheduled downloads
- [ ] Download queue management
- [ ] Bandwidth limiting option

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Legal Disclaimer

This tool is for **personal use only**. Please respect copyright laws and YouTube's Terms of Service:

- ✅ **DO**: Download your own videos, Creative Commons content, public domain videos
- ✅ **DO**: Download for offline personal viewing, educational purposes
- ✅ **DO**: Download videos you have permission to download
- ❌ **DON'T**: Redistribute downloaded content without permission
- ❌ **DON'T**: Use this tool for piracy or commercial purposes
- ❌ **DON'T**: Download copyrighted content to share or sell
- ❌ **DON'T**: Circumvent paywalls or download premium content you haven't paid for

**Use responsibly and ethically.** The developers of this tool are not responsible for misuse.

---

## 🙏 Acknowledgments

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - The amazing YouTube downloader that makes this possible
- **[ffmpeg](https://ffmpeg.org/)** - The multimedia framework that powers video processing
- **Everyone who spent hours troubleshooting broken tools** - this is for you

---

## 📊 Project Stats

- **Lines of Code**: ~950
- **Dependencies**: 2 (auto-installed)
- **Platforms Supported**: 3 (Windows, macOS, Linux)
- **Interfaces**: 2 (CLI + GUI)
- **Download Modes**: 6 (Single, Sequential, Parallel, Range, Quality, List)
- **Time Saved**: Hours of your life
- **Speed Boost**: 3-5x faster with parallel downloads

---

## 🚀 Quick Reference Card

```bash
# Install Python (if needed)
# Windows: python.org (CHECK "Add to PATH")
# macOS: brew install python3
# Linux: sudo apt install python3 python3-pip

# Clone repository
git clone https://github.com/patrick-paul/Playlistify.git
cd Playlistify

# Run script
python playlist_downloader.py

# Choose interface
1 = CLI (terminal)
2 = GUI (graphical)

# CLI Options
1 = List videos only (preview)
2 = Sequential download (safe)
3 = Parallel download (fast) ⭐ RECOMMENDED
4 = Video range (specific videos)
5 = Custom quality

# Recommended settings
Workers: 3-5
Quality: 1080p
Mode: Parallel
```

---

**Made with 😤 frustration and ☕ coffee after wasting 2 hours on tools that don't work.**

**Enhanced with ⚡ parallel downloads, 🎨 GUI, and 🔄 auto-retry for ultimate reliability.**

If this saved you time, give it a ⭐ and share it with others!

## 📬 Contact

Questions? Suggestions? Found a bug?
- **Issues**: [GitHub Issues](https://github.com/patrick-paul/Playlistify/issues)
- **Discussions**: [GitHub Discussions](https://github.com/patrick-paul/Playlistify/discussions)
- **Email**: [Your email if you want to add it]

---

**Remember**: Your time is valuable. Don't waste it on broken tools. 🚀

**Pro tip**: Bookmark this page - you'll want to come back to it!