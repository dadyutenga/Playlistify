#!/usr/bin/env python3
"""
YouTube Music Downloader + Tag Editor
Download music from YouTube and automatically add metadata (title, artist, album, cover art)
Features: MP3 conversion, auto-tagging, batch processing, drag & drop, metadata fixing
"""

import subprocess
import sys
import json
import os
import re
import shutil
from pathlib import Path
from urllib.request import urlretrieve, Request, urlopen
from concurrent.futures import ThreadPoolExecutor, as_completed

# Install required packages
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("Installing colorama...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'colorama'])
    from colorama import init, Fore, Style
    init(autoreset=True)

try:
    from tqdm import tqdm
except ImportError:
    print("Installing tqdm...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tqdm'])
    from tqdm import tqdm

try:
    from mutagen.easyid3 import EasyID3
    from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TDRC, TCON
    from mutagen.mp3 import MP3
except ImportError:
    print("Installing mutagen for MP3 tagging...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'mutagen'])
    from mutagen.easyid3 import EasyID3
    from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TDRC, TCON
    from mutagen.mp3 import MP3

try:
    import requests
except ImportError:
    print("Installing requests...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
    import requests

# Color helpers
GREEN = Fore.GREEN + Style.BRIGHT
YELLOW = Fore.YELLOW + Style.BRIGHT
RED = Fore.RED + Style.BRIGHT
CYAN = Fore.CYAN + Style.BRIGHT
MAGENTA = Fore.MAGENTA + Style.BRIGHT
WHITE = Fore.WHITE + Style.BRIGHT
RESET = Style.RESET_ALL

# Emoji constants
SUCCESS = GREEN + "✓"
WARNING = YELLOW + "⚠"
ERROR = RED + "✗"
INFO = CYAN + "ℹ"
MUSIC = MAGENTA + "♪"
TAG = CYAN + "🏷"


def check_dependencies():
    """Check and install all required dependencies"""
    print(f"\n{'=' * 60}")
    print(f"{WHITE}Checking dependencies...")
    print(f"{'=' * 60}\n")
    
    dependencies = {
        'yt-dlp': 'YouTube downloader',
        'ffmpeg': 'Audio converter',
        'mutagen': 'MP3 tag editor',
    }
    
    all_good = True
    
    # Check yt-dlp
    print(f"[1/3] {INFO} Checking yt-dlp...")
    if shutil.which('yt-dlp'):
        print(f"  {SUCCESS} yt-dlp installed")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'yt-dlp'], 
                         capture_output=True, timeout=30)
        except:
            pass
    else:
        print(f"  {WARNING} Installing yt-dlp...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'yt-dlp'])
        print(f"  {SUCCESS} yt-dlp installed")
    
    # Check ffmpeg
    print(f"\n[2/3] {INFO} Checking ffmpeg...")
    if shutil.which('ffmpeg'):
        print(f"  {SUCCESS} ffmpeg installed")
    else:
        print(f"  {ERROR} ffmpeg not found!")
        print(f"  {INFO} Please install ffmpeg to convert audio to MP3")
        print(f"  {INFO} Run playlist_downloader.py first to auto-install ffmpeg")
        all_good = False
    
    # Check mutagen
    print(f"\n[3/3] {INFO} Checking mutagen...")
    try:
        import mutagen
        print(f"  {SUCCESS} mutagen installed")
    except ImportError:
        print(f"  {WARNING} Installing mutagen...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'mutagen'])
        print(f"  {SUCCESS} mutagen installed")
    
    print(f"\n{'=' * 60}")
    if all_good:
        print(f"{SUCCESS} All dependencies ready!")
    else:
        print(f"{WARNING} Some dependencies missing - some features may not work")
    print(f"{'=' * 60}\n")
    
    return all_good


def download_youtube_audio(url, output_dir='music', use_cookies=None):
    """Download audio from YouTube in best quality"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print(f"\n{MUSIC} Downloading audio from YouTube...")
    
    # Build command
    cmd = [
        'yt-dlp',
        '-x',  # Extract audio
        '--audio-format', 'mp3',
        '--audio-quality', '0',  # Best quality
        '--embed-thumbnail',  # Try to embed thumbnail
        '--add-metadata',  # Add metadata from YouTube
        '-o', f'{output_dir}/%(title)s.%(ext)s',
        '--newline',
        '--restrict-filenames',
    ]
    
    # Add cookie support for bot detection bypass
    if use_cookies:
        cmd.extend(['--cookies-from-browser', use_cookies])
    else:
        cmd.extend([
            '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            '--extractor-args', 'youtube:player_client=android,web',
            '--no-check-certificate',
        ])
    
    cmd.append(url)
    
    try:
        print(f"  {INFO} Starting download (this may take a moment)...")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 text=True, bufsize=1)
        
        pbar = None
        for line in process.stdout:
            line = line.strip()
            if line:
                if '[download]' in line and '%' in line:
                    if not pbar:
                        pbar = tqdm(total=100, desc="Downloading", 
                                  bar_format="{l_bar}{bar}| {percentage:3.0f}%")
                    try:
                        percent = float(line.split('%')[0].split()[-1])
                        pbar.update(percent - pbar.n)
                    except:
                        pass
                elif '[ExtractAudio]' in line or '[ffmpeg]' in line:
                    if pbar:
                        pbar.close()
                        pbar = None
                    print(f"  {INFO} Converting to MP3...")
                elif line and not line.startswith('['):
                    if pbar:
                        pbar.close()
                        pbar = None
        
        if pbar:
            pbar.close()
        
        process.wait()
        
        if process.returncode == 0:
            print(f"{SUCCESS} Download complete!")
            # Find the downloaded file
            mp3_files = list(Path(output_dir).glob("*.mp3"))
            if mp3_files:
                # Return the most recently created file
                return max(mp3_files, key=lambda p: p.stat().st_ctime)
            return None
        else:
            print(f"\n{ERROR} Download failed!")
            if not use_cookies:
                print(f"{WARNING} YouTube is blocking the request (bot detection)")
                print(f"{INFO} Try again and select a browser (Chrome, Firefox, Edge)")
                print(f"{INFO} Make sure you're logged into YouTube in that browser!")
            return None
            
    except Exception as e:
        print(f"{ERROR} Error: {e}")
        return None


def fetch_metadata_from_youtube(url):
    """Fetch metadata from YouTube video"""
    print(f"\n{INFO} Fetching metadata from YouTube...")
    
    try:
        cmd = [
            'yt-dlp',
            '--dump-json',
            '--no-playlist',
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            
            # Extract metadata
            title = data.get('title', '')
            uploader = data.get('uploader', '') or data.get('channel', '')
            thumbnail = data.get('thumbnail')
            
            # Try to parse artist and title from video title
            # Common patterns: "Artist - Title", "Title - Artist", "Artist: Title"
            artist = uploader
            song_title = title
            
            patterns = [
                r'^(.+?)\s*[-–—]\s*(.+)$',  # Artist - Title or Title - Artist
                r'^(.+?)\s*:\s*(.+)$',       # Artist: Title
                r'^(.+?)\s*\|\s*(.+)$',      # Artist | Title
            ]
            
            for pattern in patterns:
                match = re.match(pattern, title)
                if match:
                    part1, part2 = match.groups()
                    # Heuristic: artist is usually shorter or is the uploader name
                    if uploader.lower() in part1.lower():
                        artist = part1.strip()
                        song_title = part2.strip()
                    elif uploader.lower() in part2.lower():
                        artist = part2.strip()
                        song_title = part1.strip()
                    else:
                        # Assume format is Artist - Title
                        artist = part1.strip()
                        song_title = part2.strip()
                    break
            
            # Remove common suffixes
            suffixes = [
                r'\s*\(official\s+(?:music\s+)?video\)',
                r'\s*\(official\s+audio\)',
                r'\s*\(lyric\s+video\)',
                r'\s*\[official\]',
                r'\s*\(hd\)',
                r'\s*\(hq\)',
            ]
            
            for suffix in suffixes:
                song_title = re.sub(suffix, '', song_title, flags=re.IGNORECASE)
                artist = re.sub(suffix, '', artist, flags=re.IGNORECASE)
            
            metadata = {
                'title': song_title.strip(),
                'artist': artist.strip(),
                'album': '',
                'year': str(data.get('upload_date', '')[:4]) if data.get('upload_date') else '',
                'thumbnail': thumbnail,
            }
            
            print(f"  {SUCCESS} Metadata retrieved")
            print(f"    Title: {metadata['title']}")
            print(f"    Artist: {metadata['artist']}")
            
            return metadata
        else:
            return None
            
    except Exception as e:
        print(f"  {WARNING} Could not fetch metadata: {e}")
        return None


def download_cover_art(thumbnail_url, output_path):
    """Download cover art from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(thumbnail_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        return False
    except Exception as e:
        print(f"  {WARNING} Could not download cover art: {e}")
        return False


def apply_metadata(mp3_file, metadata, cover_art_path=None):
    """Apply metadata tags to MP3 file"""
    print(f"\n{TAG} Applying metadata tags...")
    
    try:
        # Load the MP3 file
        audio = MP3(mp3_file, ID3=ID3)
        
        # Try to load existing tags, if it fails, create new ones
        try:
            if audio.tags is None:
                audio.add_tags()
        except:
            # Tags might exist but be corrupted, try to delete and recreate
            try:
                audio.delete()
                audio.save()
                audio = MP3(mp3_file)
                audio.add_tags()
            except:
                pass
        
        # Now we have clean tags, set the metadata
        # Clear specific fields we're going to set
        if metadata.get('title'):
            audio.tags.delall('TIT2')
            audio.tags.add(TIT2(encoding=3, text=metadata['title']))
        
        if metadata.get('artist'):
            audio.tags.delall('TPE1')
            audio.tags.add(TPE1(encoding=3, text=metadata['artist']))
        
        if metadata.get('album'):
            audio.tags.delall('TALB')
            audio.tags.add(TALB(encoding=3, text=metadata['album']))
        
        if metadata.get('year'):
            audio.tags.delall('TDRC')
            audio.tags.add(TDRC(encoding=3, text=metadata['year']))
        
        if metadata.get('genre'):
            audio.tags.delall('TCON')
            audio.tags.add(TCON(encoding=3, text=metadata['genre']))
        
        # Add cover art
        if cover_art_path and Path(cover_art_path).exists():
            # Remove existing cover art first
            audio.tags.delall('APIC')
            
            with open(cover_art_path, 'rb') as img:
                audio.tags.add(
                    APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3,  # Cover (front)
                        desc='Cover',
                        data=img.read()
                    )
                )
            print(f"  {SUCCESS} Cover art embedded")
        
        audio.save(v2_version=3)
        
        print(f"  {SUCCESS} Metadata applied successfully!")
        return True
        
    except Exception as e:
        print(f"  {ERROR} Failed to apply metadata: {e}")
        import traceback
        traceback.print_exc()
        return False


def read_metadata(mp3_file):
    """Read metadata from MP3 file"""
    try:
        audio = MP3(mp3_file, ID3=ID3)
        
        metadata = {
            'title': '',
            'artist': '',
            'album': '',
            'year': '',
            'genre': '',
        }
        
        if audio.tags:
            metadata['title'] = str(audio.tags.get('TIT2', ''))
            metadata['artist'] = str(audio.tags.get('TPE1', ''))
            metadata['album'] = str(audio.tags.get('TALB', ''))
            metadata['year'] = str(audio.tags.get('TDRC', ''))
            metadata['genre'] = str(audio.tags.get('TCON', ''))
        
        return metadata
        
    except Exception as e:
        print(f"  {ERROR} Could not read metadata: {e}")
        return None


def fix_mp3_metadata(mp3_file):
    """Interactive metadata editor for a single MP3 file"""
    print(f"\n{'=' * 60}")
    print(f"{TAG} Fix MP3 Metadata: {Path(mp3_file).name}")
    print(f"{'=' * 60}\n")
    
    if not Path(mp3_file).exists():
        print(f"{ERROR} File not found: {mp3_file}")
        return False
    
    # Read current metadata
    print(f"{INFO} Current metadata:")
    current = read_metadata(mp3_file)
    
    if current:
        print(f"  Title:  {current['title'] or '(empty)'}")
        print(f"  Artist: {current['artist'] or '(empty)'}")
        print(f"  Album:  {current['album'] or '(empty)'}")
        print(f"  Year:   {current['year'] or '(empty)'}")
        print(f"  Genre:  {current['genre'] or '(empty)'}")
    
    print(f"\n{INFO} Enter new metadata (press Enter to keep current value):\n")
    
    # Get new metadata
    new_metadata = {}
    
    title = input(f"  Title [{current.get('title', '')}]: ").strip()
    new_metadata['title'] = title if title else current.get('title', '')
    
    artist = input(f"  Artist [{current.get('artist', '')}]: ").strip()
    new_metadata['artist'] = artist if artist else current.get('artist', '')
    
    album = input(f"  Album [{current.get('album', '')}]: ").strip()
    new_metadata['album'] = album if album else current.get('album', '')
    
    year = input(f"  Year [{current.get('year', '')}]: ").strip()
    new_metadata['year'] = year if year else current.get('year', '')
    
    genre = input(f"  Genre [{current.get('genre', '')}]: ").strip()
    new_metadata['genre'] = genre if genre else current.get('genre', '')
    
    # Ask about cover art
    cover_path = input(f"\n  Cover art path (press Enter to skip): ").strip()
    if cover_path and not Path(cover_path).exists():
        print(f"  {WARNING} Cover art file not found, skipping...")
        cover_path = None
    
    # Apply metadata
    return apply_metadata(mp3_file, new_metadata, cover_path)


def batch_process_folder(folder_path, auto_tag=True):
    """Process all MP3 files in a folder"""
    print(f"\n{'=' * 60}")
    print(f"{MUSIC} Batch Processing: {folder_path}")
    print(f"{'=' * 60}\n")
    
    folder = Path(folder_path)
    if not folder.exists():
        print(f"{ERROR} Folder not found: {folder_path}")
        return
    
    mp3_files = list(folder.glob("*.mp3"))
    
    if not mp3_files:
        print(f"{WARNING} No MP3 files found in folder")
        return
    
    print(f"{INFO} Found {len(mp3_files)} MP3 file(s)\n")
    
    if auto_tag:
        print(f"{INFO} Auto-tagging based on filename...\n")
    
    for mp3_file in mp3_files:
        print(f"\n{MUSIC} Processing: {mp3_file.name}")
        
        if auto_tag:
            # Try to parse filename: "Artist - Title.mp3"
            filename = mp3_file.stem
            
            metadata = {
                'title': filename,
                'artist': '',
                'album': '',
                'year': '',
                'genre': '',
            }
            
            patterns = [
                r'^(.+?)\s*[-–—]\s*(.+)$',
                r'^(.+?)\s*:\s*(.+)$',
                r'^(\d+)\s*[-.)]\s*(.+?)\s*[-–—]\s*(.+)$',  # Track - Artist - Title
            ]
            
            for pattern in patterns:
                match = re.match(pattern, filename)
                if match:
                    groups = match.groups()
                    if len(groups) == 2:
                        metadata['artist'] = groups[0].strip()
                        metadata['title'] = groups[1].strip()
                    elif len(groups) == 3:
                        metadata['artist'] = groups[1].strip()
                        metadata['title'] = groups[2].strip()
                    break
            
            print(f"  Detected - Artist: {metadata['artist']}, Title: {metadata['title']}")
            
            apply_metadata(mp3_file, metadata)
        else:
            # Manual editing
            fix_mp3_metadata(str(mp3_file))
    
    print(f"\n{'=' * 60}")
    print(f"{SUCCESS} Batch processing complete!")
    print(f"{'=' * 60}\n")


def download_and_tag(url, output_dir='music', use_cookies=None):
    """Download YouTube audio and automatically tag it"""
    
    # Fetch metadata first
    metadata = fetch_metadata_from_youtube(url)
    
    # Download audio
    mp3_file = download_youtube_audio(url, output_dir, use_cookies)
    
    if not mp3_file:
        print(f"{ERROR} Download failed")
        return False
    
    # Download cover art
    cover_art_path = None
    if metadata and metadata.get('thumbnail'):
        cover_art_path = Path(output_dir) / 'temp_cover.jpg'
        if download_cover_art(metadata['thumbnail'], cover_art_path):
            print(f"  {SUCCESS} Cover art downloaded")
        else:
            print(f"  {WARNING} Could not download cover art")
            cover_art_path = None
    
    # Apply metadata
    if metadata:
        success = apply_metadata(mp3_file, metadata, cover_art_path)
        
        # Verify tags were applied
        if success:
            print(f"\n{INFO} Verifying tags...")
            try:
                audio = MP3(mp3_file, ID3=ID3)
                has_title = bool(audio.tags and audio.tags.get('TIT2'))
                has_artist = bool(audio.tags and audio.tags.get('TPE1'))
                has_cover = bool(audio.tags and audio.tags.get('APIC:Cover'))
                
                if has_title:
                    print(f"  {SUCCESS} Title: {audio.tags.get('TIT2')}")
                if has_artist:
                    print(f"  {SUCCESS} Artist: {audio.tags.get('TPE1')}")
                if has_cover:
                    print(f"  {SUCCESS} Cover art: Embedded")
                
                if not (has_title or has_artist):
                    print(f"  {WARNING} Tags may not have been saved properly")
            except Exception as e:
                print(f"  {WARNING} Could not verify tags: {e}")
    
    # Cleanup temp cover art
    if cover_art_path and Path(cover_art_path).exists():
        try:
            Path(cover_art_path).unlink()
        except:
            pass
    
    print(f"\n{'=' * 60}")
    print(f"{SUCCESS} Music file ready: {mp3_file.name}")
    print(f"{INFO} Location: {mp3_file.absolute()}")
    print(f"{'=' * 60}\n")
    
    return True


def main():
    """Main function"""
    print(f"\n{'=' * 70}")
    print(f"{MUSIC} {WHITE}YouTube Music Downloader + Tag Editor")
    print(f"{'=' * 70}\n")
    
    # Check dependencies
    if not check_dependencies():
        print(f"\n{WARNING} Please install missing dependencies first")
        print(f"{INFO} Run 'python playlist_downloader.py' to auto-install ffmpeg")
        return
    
    while True:
        print(f"\n{'=' * 70}")
        print(f"{WHITE}What would you like to do?")
        print(f"{CYAN}1. Download music from YouTube (MP3 + auto-tag)")
        print(f"{CYAN}2. Fix metadata for a single MP3 file")
        print(f"{CYAN}3. Batch process folder (auto-tag all MP3s)")
        print(f"{CYAN}4. Batch process folder (manual edit each)")
        print(f"{CYAN}5. Exit")
        print(f"{'=' * 70}")
        
        choice = input(f"\n{INFO} Enter choice (1-5): {RESET}").strip()
        
        if choice == '1':
            url = input(f"\n{MUSIC} Enter YouTube URL: {RESET}").strip()
            
            if not url:
                print(f"{ERROR} No URL provided")
                continue
            
            output_dir = input(f"{INFO} Output folder (press Enter for 'music'): {RESET}").strip()
            if not output_dir:
                output_dir = 'music'
            
            # Browser cookies for bot detection
            print(f"\n{YELLOW}🔒 Browser cookies (RECOMMENDED to avoid bot detection):")
            print(f"{CYAN}  1. Chrome   {GREEN}← Recommended")
            print(f"{CYAN}  2. Firefox")
            print(f"{CYAN}  3. Edge")
            print(f"{CYAN}  4. Brave")
            print(f"{CYAN}  5. Opera")
            print(f"{RED}  6. None (may fail)")
            
            browser_choice = input(f"\n{INFO} Select browser (1-6, press Enter for Chrome): {RESET}").strip()
            browser_map = {
                '1': 'chrome',
                '2': 'firefox',
                '3': 'edge',
                '4': 'brave',
                '5': 'opera',
                '6': None,
                '': 'chrome'
            }
            use_cookies = browser_map.get(browser_choice, 'chrome')
            
            if use_cookies:
                print(f"{SUCCESS} Using cookies from: {use_cookies.upper()}")
                print(f"{INFO} Make sure you're logged into YouTube in {use_cookies.capitalize()}!")
            else:
                print(f"{WARNING} No cookies selected - download may fail due to bot detection")
                print(f"{INFO} If it fails, try again with browser cookies")
            
            download_and_tag(url, output_dir, use_cookies)
        
        elif choice == '2':
            mp3_file = input(f"\n{TAG} Enter MP3 file path (or drag & drop): {RESET}").strip()
            
            # Remove quotes from drag & drop
            mp3_file = mp3_file.strip('"').strip("'")
            
            if not mp3_file:
                print(f"{ERROR} No file provided")
                continue
            
            fix_mp3_metadata(mp3_file)
        
        elif choice == '3':
            folder = input(f"\n{MUSIC} Enter folder path (or drag & drop): {RESET}").strip()
            folder = folder.strip('"').strip("'")
            
            if not folder:
                print(f"{ERROR} No folder provided")
                continue
            
            batch_process_folder(folder, auto_tag=True)
        
        elif choice == '4':
            folder = input(f"\n{MUSIC} Enter folder path (or drag & drop): {RESET}").strip()
            folder = folder.strip('"').strip("'")
            
            if not folder:
                print(f"{ERROR} No folder provided")
                continue
            
            batch_process_folder(folder, auto_tag=False)
        
        elif choice == '5':
            print(f"\n{SUCCESS} Thanks for using Music Downloader + Tag Editor!")
            break
        
        else:
            print(f"{ERROR} Invalid choice")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{INFO} Exiting...")
        sys.exit(0)
