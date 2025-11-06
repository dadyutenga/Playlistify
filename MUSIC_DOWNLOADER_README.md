# 🎧 YouTube Music Downloader + Tag Editor

**Download music from YouTube as MP3 with automatic metadata tagging!**

## ✨ Features

### 🎵 Download & Convert
- ✅ Download audio from YouTube
- ✅ Convert to high-quality MP3 (320kbps)
- ✅ Extract best audio quality available
- ✅ Browser cookie support (bypass bot detection)

### 🏷️ Auto-Tagging
- ✅ Automatically extract metadata from YouTube
- ✅ Smart title/artist parsing
- ✅ Download & embed cover art (album artwork)
- ✅ Add album, year, genre tags
- ✅ Clean formatting (remove "Official Video" etc.)

### 🛠️ Metadata Editor
- ✅ Fix metadata for existing MP3 files
- ✅ Interactive editing interface
- ✅ Batch process entire folders
- ✅ Auto-tag from filename patterns
- ✅ Manual edit mode for precision

### 📁 Batch Processing
- ✅ Process entire folders at once
- ✅ Auto-detect artist/title from filenames
- ✅ Support for common naming patterns
- ✅ Manual review option

### 🖱️ User-Friendly
- ✅ Drag & drop support
- ✅ Progress bars
- ✅ Colored output
- ✅ Error handling & retries

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+** (same as playlist downloader)
- **ffmpeg** (install using `playlist_downloader.py` first)

### Installation

1. **Clone the repo** (if you haven't already):
   ```bash
   git clone https://github.com/dadyutenga/Playlistify.git
   cd Playlistify
   ```

2. **Run the music downloader**:
   ```bash
   python music_downloader.py
   ```

3. **Dependencies auto-install**:
   - yt-dlp (YouTube downloader)
   - mutagen (MP3 tag editor)
   - requests (cover art download)
   - colorama, tqdm (UI)

---

## 📖 Usage Guide

### 1️⃣ Download Music from YouTube

```bash
$ python music_downloader.py
```

**Select option 1: Download music from YouTube**

**Example:**
```
Enter YouTube URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Output folder: my_music
Select browser (1-4): 1

♪ Downloading audio from YouTube...
Downloading: 100%|████████████| 100%
✓ Download complete!

ℹ Fetching metadata from YouTube...
  ✓ Metadata retrieved
    Title: Never Gonna Give You Up
    Artist: Rick Astley

🏷 Applying metadata tags...
  ✓ Cover art embedded
  ✓ Metadata applied successfully!

✓ Music file ready: Never_Gonna_Give_You_Up.mp3
```

**What it does:**
- Downloads audio in best quality
- Converts to MP3 (320kbps)
- Extracts artist & title from video
- Downloads cover art
- Embeds all metadata in MP3

---

### 2️⃣ Fix Metadata for Single MP3

**Perfect for files with wrong or missing tags!**

```bash
What would you like to do?
2. Fix metadata for a single MP3 file

Enter MP3 file path: C:\Music\song.mp3
# Or drag & drop the file!
```

**Interactive editor:**
```
Current metadata:
  Title:  Unknown Song
  Artist: (empty)
  Album:  (empty)
  Year:   (empty)
  Genre:  (empty)

Enter new metadata (press Enter to keep current):
  Title [Unknown Song]: Never Gonna Give You Up
  Artist []: Rick Astley
  Album []: Whenever You Need Somebody
  Year []: 1987
  Genre []: Pop

  Cover art path (press Enter to skip): cover.jpg

✓ Metadata applied successfully!
```

---

### 3️⃣ Batch Process Folder (Auto-Tag)

**Process all MP3 files in a folder automatically!**

Supports these filename patterns:
- `Artist - Title.mp3`
- `Artist: Title.mp3`
- `01 - Artist - Title.mp3`
- `Track Number. Title.mp3`

```bash
What would you like to do?
3. Batch process folder (auto-tag all MP3s)

Enter folder path: C:\Music\Downloads
# Or drag & drop the folder!

Found 25 MP3 file(s)

♪ Processing: Rick_Astley_-_Never_Gonna_Give_You_Up.mp3
  Detected - Artist: Rick Astley, Title: Never Gonna Give You Up
  ✓ Metadata applied successfully!

♪ Processing: Queen_-_Bohemian_Rhapsody.mp3
  Detected - Artist: Queen, Title: Bohemian Rhapsody
  ✓ Metadata applied successfully!

...

✓ Batch processing complete!
```

---

### 4️⃣ Batch Process (Manual Edit)

**For precision control over each file:**

```bash
What would you like to do?
4. Batch process folder (manual edit each)

Enter folder path: C:\Music\Downloads
```

This will go through each MP3 file and let you edit metadata interactively.

---

## 🎯 Common Use Cases

### Use Case 1: Download Your Favorite Songs

```bash
python music_downloader.py
# Choose option 1
# Paste YouTube URL
# Done! MP3 with cover art ready
```

### Use Case 2: Fix iTunes/Spotify Rips

You downloaded songs but they have wrong metadata:

```bash
python music_downloader.py
# Choose option 2 (single file)
# Or option 3 (batch)
# Drag & drop files
# Enter correct info
```

### Use Case 3: Organize Music Library

You have hundreds of MP3s with messy tags:

```bash
# Rename files to: Artist - Title.mp3
# Run batch auto-tag
python music_downloader.py
# Choose option 3
# Drag & drop folder
# All files tagged instantly!
```

### Use Case 4: Download Entire Albums

Combine with `playlist_downloader.py`:

```bash
# First, get playlist of album
python playlist_downloader.py
# Choose audio-only download

# Then batch tag
python music_downloader.py
# Choose option 3 for auto-tagging
```

---

## �️ Advanced Features

### Verify MP3 Tags

Use the included verification tool to check if tags were properly applied:

```bash
python check_mp3_tags.py your_song.mp3
```

**Output example:**
```
======================================================================
📁 File: Rick_Astley_-_Never_Gonna_Give_You_Up.mp3
======================================================================

✓ Title:  Never Gonna Give You Up
✓ Artist: Rick Astley
✗ Album:  (not set)
✓ Year:   1987
✓ Cover Art: Embedded (45231 bytes)

──────────────────────────────────────────────────────────────────────
Summary: 4/5 metadata fields set
======================================================================
```

Or drag & drop the file when prompted.

### Browser Cookie Support

Just like the video downloader, this supports browser cookies to bypass YouTube bot detection:

- Chrome
- Firefox  
- Edge
- Brave
- Opera

**Make sure you're logged into YouTube in your browser!**

---

### Metadata Fields Supported

- **Title** - Song name
- **Artist** - Performer/band
- **Album** - Album name
- **Year** - Release year
- **Genre** - Music genre
- **Cover Art** - Album artwork (embedded as JPEG)

---

### Smart Title Parsing

The script intelligently parses YouTube video titles:

**Input:** `Rick Astley - Never Gonna Give You Up (Official Video)`

**Parsed:**
- Artist: Rick Astley
- Title: Never Gonna Give You Up

**Removes common patterns:**
- (Official Video)
- (Official Audio)
- [Official]
- (Lyric Video)
- (HD)
- (HQ)

---

### Filename Pattern Recognition

For batch processing, recognizes:

```
Pattern 1: Artist - Title.mp3
Pattern 2: Artist: Title.mp3
Pattern 3: Artist | Title.mp3
Pattern 4: 01 - Artist - Title.mp3
Pattern 5: 01. Artist - Title.mp3
```

---

## 🎨 Output Format

### Directory Structure

```
music/
├── Rick_Astley_-_Never_Gonna_Give_You_Up.mp3
├── Queen_-_Bohemian_Rhapsody.mp3
└── The_Beatles_-_Hey_Jude.mp3
```

### MP3 File Contents

Each MP3 includes:
- ✅ High-quality audio (320kbps MP3)
- ✅ ID3v2 tags (universal compatibility)
- ✅ Embedded cover art
- ✅ Complete metadata

**Compatible with:**
- iTunes/Apple Music
- Spotify local files
- Windows Media Player
- VLC
- Car audio systems
- Any MP3 player

---

## 🐛 Troubleshooting

### Issue: "ffmpeg not found"

**Solution:**
```bash
# Run the video downloader first
python playlist_downloader.py
# It will auto-install ffmpeg

# Or install manually:
# Windows: winget install Gyan.FFmpeg
# Mac: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

### Issue: "Bot detection / HTTP 429"

**Solution:** Use browser cookies!
- Make sure you're logged into YouTube in your browser
- Select your browser when prompted (Chrome, Firefox, etc.)
- Keep browser open during download

### Issue: "No metadata found"

**Solution:** 
- The video might have unusual title formatting
- Use option 2 to manually edit metadata
- Or rename file and use batch auto-tag

### Issue: "Failed to apply metadata: an ID3 tag already exists"

**Solution:** This is now fixed in the latest version!
- The script now properly handles existing ID3 tags from yt-dlp
- It will update/replace existing tags instead of failing
- If you still see this, update your script to the latest version

### Issue: "Cover art not embedded"

**Solution:**
- Check internet connection (needs to download image)
- Some videos don't have thumbnails
- Run the tag verification: `python check_mp3_tags.py your_file.mp3`
- You can manually add later with option 2

### Issue: "Corrupted MP3 file"

**Solution:**
- Check disk space
- Update yt-dlp: `pip install --upgrade yt-dlp`
- Update ffmpeg to latest version
- Try downloading again

---

## 📊 Comparison with Other Tools

| Feature | This Script | Online Tools | Paid Software |
|---------|------------|--------------|---------------|
| **Price** | Free | Free (limited) | $20-50 |
| **Quality** | 320kbps MP3 | Usually 128kbps | 320kbps |
| **Auto-tagging** | ✅ Yes | ❌ No | ✅ Yes |
| **Cover art** | ✅ Embedded | ❌ No | ✅ Yes |
| **Batch process** | ✅ Yes | ❌ No | ✅ Yes |
| **Privacy** | ✅ Local | ⚠️ Upload required | ✅ Local |
| **No limits** | ✅ Unlimited | ❌ Daily limits | ✅ Unlimited |

---

## 🤝 Contributing

Ideas for improvements:

- [ ] Fetch lyrics from Genius/MusixMatch
- [ ] Support for Apple Music metadata
- [ ] Spotify playlist import
- [ ] BPM detection
- [ ] Duplicate detection
- [ ] Smart playlist generator
- [ ] GUI interface (drag & drop window)
- [ ] Integration with music library apps
- [ ] SoundCloud support
- [ ] Bandcamp support

---

## ⚠️ Legal Disclaimer

**For personal use only.**

- Only download music you have permission to download
- Respect copyright laws
- Don't redistribute downloaded content
- Don't use for commercial purposes
- Support artists by buying their music

**Use responsibly and ethically.**

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file

---

## 🙏 Credits

- **yt-dlp** - YouTube download engine
- **ffmpeg** - Audio conversion
- **mutagen** - MP3 tag editing
- **You** - For supporting open source!

---

## 💡 Tips & Tricks

### Tip 1: Best Quality Downloads
The script automatically selects the best available quality. YouTube Music uploads are usually 256kbps AAC, which converts cleanly to 320kbps MP3.

### Tip 2: Organizing Your Library
Use this filename structure for best results:
```
Artist - Song Title.mp3
```

Then run batch auto-tag to fix all tags at once!

### Tip 3: Cover Art Sources
If auto-download fails, you can:
- Google "album name cover art"
- Use iTunes artwork
- Visit MusicBrainz or Last.fm
- Then add manually with option 2

### Tip 4: Multiple Versions
Downloading the same song in different quality? Name them:
```
Song Title (320kbps).mp3
Song Title (128kbps).mp3
```

### Tip 5: Playlist Management
Combine with the video downloader:
```bash
# Download entire YouTube Music playlist
python playlist_downloader.py
# (Choose audio extraction)

# Then batch tag all files
python music_downloader.py
# (Option 3: Batch auto-tag)
```

---

**Made with 🎵 and ☕**

**If this saved you time and money, give it a ⭐!**
