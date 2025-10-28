#!/usr/bin/env python3
"""
YouTube Playlist Downloader - Enhanced Version
Downloads videos/playlists from YouTube using yt-dlp
Features: Single video, progress bars, parallel downloads, GUI, range selection, auto-retry
"""

import subprocess
import sys
import json
import os
import platform
import zipfile
import shutil
import threading
import time
from pathlib import Path
from urllib.request import urlretrieve
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_os():
    """Detect the operating system"""
    system = platform.system().lower()
    if system == 'windows':
        return 'windows'
    elif system == 'darwin':
        return 'mac'
    elif system == 'linux':
        return 'linux'
    else:
        return 'unknown'

def check_command_exists(command):
    """Check if a command exists in PATH"""
    try:
        subprocess.run([command, '--version'], 
                      capture_output=True, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_ytdlp():
    """Install yt-dlp using pip"""
    print("Installing yt-dlp...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'yt-dlp'])
        print("✓ yt-dlp installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install yt-dlp. Please install manually:")
        print("  pip install yt-dlp")
        return False

def add_to_windows_path(directory):
    """Add directory to Windows PATH (requires admin rights)"""
    try:
        import winreg
        
        # Get current PATH
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_ALL_ACCESS)
        current_path, _ = winreg.QueryValueEx(key, 'PATH')
        
        # Check if already in PATH
        if directory.lower() in current_path.lower():
            print(f"  Already in PATH: {directory}")
            return True
        
        # Add to PATH
        new_path = f"{current_path};{directory}"
        winreg.SetValueEx(key, 'PATH', 0, winreg.REG_EXPAND_SZ, new_path)
        winreg.CloseKey(key)
        
        # Update current process environment
        os.environ['PATH'] = f"{os.environ['PATH']};{directory}"
        
        print(f"  ✓ Added to PATH: {directory}")
        print("  Note: You may need to restart your terminal for changes to take effect")
        return True
    except Exception as e:
        print(f"  ✗ Could not add to PATH automatically: {e}")
        print(f"  Please add manually: {directory}")
        return False

def install_ffmpeg_windows():
    """Install ffmpeg on Windows"""
    print("\nInstalling ffmpeg for Windows...")
    
    # Check common installation methods
    if shutil.which('winget'):
        print("  Attempting installation via winget...")
        try:
            subprocess.run(['winget', 'install', 'Gyan.FFmpeg', '--silent'], check=True)
            print("  ✓ ffmpeg installed via winget!")
            return True
        except subprocess.CalledProcessError:
            print("  winget installation failed, trying manual installation...")
    
    if shutil.which('choco'):
        print("  Attempting installation via chocolatey...")
        try:
            subprocess.run(['choco', 'install', 'ffmpeg', '-y'], check=True)
            print("  ✓ ffmpeg installed via chocolatey!")
            return True
        except subprocess.CalledProcessError:
            print("  chocolatey installation failed, trying manual installation...")
    
    # Manual installation
    print("  Downloading ffmpeg manually...")
    try:
        ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        install_dir = Path.home() / "ffmpeg"
        zip_path = install_dir / "ffmpeg.zip"
        
        install_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"  Downloading from {ffmpeg_url}...")
        urlretrieve(ffmpeg_url, zip_path)
        
        print("  Extracting...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(install_dir)
        
        # Find the bin directory
        bin_dirs = list(install_dir.glob("*/bin"))
        if bin_dirs:
            bin_dir = bin_dirs[0]
            
            # Copy executables to install_dir
            for exe in bin_dir.glob("*.exe"):
                shutil.copy2(exe, install_dir)
            
            # Add to PATH
            add_to_windows_path(str(install_dir))
            
            # Cleanup
            zip_path.unlink()
            for item in install_dir.iterdir():
                if item.is_dir() and item.name.startswith('ffmpeg-'):
                    shutil.rmtree(item)
            
            print(f"  ✓ ffmpeg installed to {install_dir}")
            return True
        
    except Exception as e:
        print(f"  ✗ Manual installation failed: {e}")
        print("\n  Please install ffmpeg manually:")
        print("  1. Download from: https://www.gyan.dev/ffmpeg/builds/")
        print("  2. Extract and add to PATH")
        return False
    
    return False

def install_ffmpeg_mac():
    """Install ffmpeg on macOS"""
    print("\nInstalling ffmpeg for macOS...")
    
    if not shutil.which('brew'):
        print("  ✗ Homebrew not found. Please install Homebrew first:")
        print("  /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        return False
    
    try:
        print("  Installing via Homebrew...")
        subprocess.run(['brew', 'install', 'ffmpeg'], check=True)
        print("  ✓ ffmpeg installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Installation failed: {e}")
        return False

def install_ffmpeg_linux():
    """Install ffmpeg on Linux"""
    print("\nInstalling ffmpeg for Linux...")
    
    # Try different package managers
    package_managers = [
        (['sudo', 'apt', 'update'], ['sudo', 'apt', 'install', '-y', 'ffmpeg']),
        (['sudo', 'yum', 'install', '-y', 'ffmpeg'], None),
        (['sudo', 'dnf', 'install', '-y', 'ffmpeg'], None),
        (['sudo', 'pacman', '-S', '--noconfirm', 'ffmpeg'], None),
    ]
    
    for commands in package_managers:
        update_cmd, install_cmd = commands if len(commands) == 2 else (None, commands[0])
        
        try:
            if update_cmd:
                subprocess.run(update_cmd, check=True, capture_output=True)
            
            subprocess.run(install_cmd, check=True)
            print("  ✓ ffmpeg installed successfully!")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    print("  ✗ Could not install ffmpeg automatically.")
    print("  Please install manually using your package manager:")
    print("    Ubuntu/Debian: sudo apt install ffmpeg")
    print("    Fedora: sudo dnf install ffmpeg")
    print("    Arch: sudo pacman -S ffmpeg")
    return False

def install_ffmpeg():
    """Install ffmpeg based on OS"""
    os_type = get_os()
    
    if os_type == 'windows':
        return install_ffmpeg_windows()
    elif os_type == 'mac':
        return install_ffmpeg_mac()
    elif os_type == 'linux':
        return install_ffmpeg_linux()
    else:
        print("✗ Unknown operating system. Please install ffmpeg manually.")
        return False

def setup_dependencies():
    """Check and install all required dependencies"""
    print("=" * 50)
    print("Checking dependencies...")
    print("=" * 50)
    
    os_type = get_os()
    print(f"\nDetected OS: {os_type}")
    
    # Check yt-dlp
    print("\n[1/2] Checking yt-dlp...")
    if check_command_exists('yt-dlp'):
        print("  ✓ yt-dlp is already installed")
        # Try to update it
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'yt-dlp'], 
                         capture_output=True, check=True)
            print("  ✓ Updated to latest version")
        except:
            pass
    else:
        if not install_ytdlp():
            return False
    
    # Check ffmpeg
    print("\n[2/2] Checking ffmpeg...")
    if check_command_exists('ffmpeg'):
        print("  ✓ ffmpeg is already installed")
    else:
        print("  ✗ ffmpeg not found")
        install = input("  Install ffmpeg now? (y/n): ").strip().lower()
        if install == 'y':
            if not install_ffmpeg():
                print("\n  Warning: Videos will download as separate audio/video files")
                print("  You'll need to merge them manually later")
        else:
            print("  Skipping ffmpeg installation")
            print("  Warning: Videos will download as separate audio/video files")
    
    print("\n" + "=" * 50)
    print("Setup complete!")
    print("=" * 50)
    return True

def get_playlist_info(playlist_url):
    """Extract playlist information and video URLs"""
    try:
        cmd = [
            'yt-dlp',
            '--flat-playlist',
            '--dump-json',
            playlist_url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                video_data = json.loads(line)
                videos.append({
                    'title': video_data.get('title', 'Unknown'),
                    'url': f"https://www.youtube.com/watch?v={video_data['id']}",
                    'id': video_data['id'],
                    'duration': video_data.get('duration', 0)
                })
        
        return videos
    except subprocess.CalledProcessError as e:
        print(f"Error fetching playlist info: {e}")
        print(f"Error output: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing playlist data: {e}")
        return None

def download_single_video(video_url, output_dir='downloads', quality='best', max_retries=3):
    """
    Download a single video with progress bar and retry logic
    
    Args:
        video_url: YouTube video URL
        output_dir: Directory to save video
        quality: Video quality
        max_retries: Maximum retry attempts on failure
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    quality_formats = {
        'best': 'bestvideo+bestaudio/best',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        'worst': 'worstvideo+worstaudio/worst'
    }
    
    format_string = quality_formats.get(quality, quality_formats['best'])
    
    cmd = [
        'yt-dlp',
        '-f', format_string,
        '--merge-output-format', 'mp4',
        '-o', f'{output_dir}/%(title)s.%(ext)s',
        '--newline',  # Progress on new lines for parsing
        '--progress',  # Show progress
        video_url
    ]
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"\nDownloading video (Attempt {attempt}/{max_retries})...")
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     text=True, bufsize=1)
            
            for line in process.stdout:
                line = line.strip()
                if '[download]' in line and '%' in line:
                    # Extract progress percentage
                    if 'ETA' in line or '%' in line:
                        print(f"\r{line}", end='', flush=True)
                elif line:
                    print(line)
            
            process.wait()
            
            if process.returncode == 0:
                print("\n✓ Download complete!")
                return True
            else:
                if attempt < max_retries:
                    print(f"\n✗ Download failed. Retrying in 3 seconds...")
                    time.sleep(3)
                else:
                    print(f"\n✗ Download failed after {max_retries} attempts")
                    return False
                    
        except KeyboardInterrupt:
            print("\n\nDownload interrupted by user")
            return False
        except Exception as e:
            if attempt < max_retries:
                print(f"\n✗ Error: {e}. Retrying in 3 seconds...")
                time.sleep(3)
            else:
                print(f"\n✗ Error after {max_retries} attempts: {e}")
                return False
    
    return False

def download_video_worker(video_info, output_dir, quality, max_retries=3):
    """Worker function for parallel downloads"""
    video_url = video_info['url']
    video_title = video_info['title']
    video_index = video_info.get('index', '')
    
    quality_formats = {
        'best': 'bestvideo+bestaudio/best',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        'worst': 'worstvideo+worstaudio/worst'
    }
    
    format_string = quality_formats.get(quality, quality_formats['best'])
    
    if video_index:
        output_template = f'{output_dir}/{video_index} - %(title)s.%(ext)s'
    else:
        output_template = f'{output_dir}/%(title)s.%(ext)s'
    
    cmd = [
        'yt-dlp',
        '-f', format_string,
        '--merge-output-format', 'mp4',
        '-o', output_template,
        '--no-progress',  # Disable progress for parallel downloads
        '--restrict-filenames',
        video_url
    ]
    
    for attempt in range(1, max_retries + 1):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
            
            if result.returncode == 0:
                return {'success': True, 'title': video_title, 'index': video_index}
            else:
                if attempt < max_retries:
                    time.sleep(3)
                else:
                    return {'success': False, 'title': video_title, 'index': video_index, 
                           'error': 'Max retries exceeded'}
                    
        except subprocess.TimeoutExpired:
            if attempt < max_retries:
                time.sleep(3)
            else:
                return {'success': False, 'title': video_title, 'index': video_index, 
                       'error': 'Timeout'}
        except Exception as e:
            if attempt < max_retries:
                time.sleep(3)
            else:
                return {'success': False, 'title': video_title, 'index': video_index, 
                       'error': str(e)}
    
    return {'success': False, 'title': video_title, 'index': video_index}

def download_playlist_parallel(playlist_url, output_dir='downloads', quality='best', 
                               max_workers=3, video_range=None):
    """
    Download playlist videos in parallel
    
    Args:
        playlist_url: YouTube playlist URL
        output_dir: Directory to save videos
        quality: Video quality
        max_workers: Number of parallel downloads (default: 3)
        video_range: Tuple (start, end) for video range, None for all
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print(f"\nFetching playlist information...")
    videos = get_playlist_info(playlist_url)
    
    if not videos:
        print("Failed to fetch playlist information.")
        return False
    
    # Apply video range filter
    if video_range:
        start, end = video_range
        start = max(1, start)
        end = min(len(videos), end)
        videos = videos[start-1:end]
        print(f"Downloading videos {start} to {end} ({len(videos)} videos)")
    else:
        print(f"Found {len(videos)} videos")
    
    # Add index to video info
    for i, video in enumerate(videos, 1):
        video['index'] = str(i + (video_range[0] - 1 if video_range else 0)).zfill(3)
    
    print(f"Starting parallel download with {max_workers} workers...")
    print(f"Output directory: {Path(output_dir).absolute()}")
    print("-" * 50)
    
    successful = 0
    failed = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_video = {
            executor.submit(download_video_worker, video, output_dir, quality): video 
            for video in videos
        }
        
        # Process completed downloads
        for future in as_completed(future_to_video):
            result = future.result()
            if result['success']:
                successful += 1
                index_str = f"[{result['index']}] " if result['index'] else ""
                print(f"✓ {index_str}{result['title']} ({successful}/{len(videos)})")
            else:
                failed.append(result)
                index_str = f"[{result['index']}] " if result['index'] else ""
                error_msg = result.get('error', 'Unknown error')
                print(f"✗ {index_str}{result['title']} - {error_msg}")
    
    print("\n" + "=" * 50)
    print(f"Download complete!")
    print(f"Successful: {successful}/{len(videos)}")
    if failed:
        print(f"Failed: {len(failed)}")
        print("\nFailed videos:")
        for video in failed:
            index_str = f"[{video['index']}] " if video['index'] else ""
            print(f"  - {index_str}{video['title']}")
    print("=" * 50)
    
    return True

def download_playlist(playlist_url, output_dir='downloads', quality='best'):
    """
    Download all videos from a playlist (sequential with progress)
    
    Args:
        playlist_url: YouTube playlist URL
        output_dir: Directory to save videos (default: 'downloads')
        quality: Video quality - 'best', '1080p', '720p', '480p', or 'worst'
    """
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Quality format selection
    quality_formats = {
        'best': 'bestvideo+bestaudio/best',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        'worst': 'worstvideo+worstaudio/worst'
    }
    
    format_string = quality_formats.get(quality, quality_formats['best'])
    
    print(f"\nDownloading playlist to: {output_dir}")
    print(f"Quality: {quality}")
    print("-" * 50)
    
    cmd = [
        'yt-dlp',
        '-f', format_string,
        '--merge-output-format', 'mp4',
        '-o', f'{output_dir}/%(playlist_index)s - %(title)s.%(ext)s',
        '--no-playlist-reverse',
        '--ignore-errors',
        '--continue',
        '--newline',
        '--restrict-filenames',
        playlist_url
    ]
    
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 text=True, bufsize=1)
        
        for line in process.stdout:
            line = line.strip()
            if line:
                if '[download]' in line and '%' in line:
                    print(f"\r{line}", end='', flush=True)
                else:
                    if '\r' in line:
                        print()  # New line after progress
                    print(line)
        
        process.wait()
        
        print("\n" + "=" * 50)
        print("Download complete!")
        print("=" * 50)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\nError during download: {e}")
        return False
    except KeyboardInterrupt:
        print("\n\nDownload interrupted by user")
        print("You can resume by running the script again with the same URL")
        return False

def list_playlist_videos(playlist_url):
    """List all videos in the playlist without downloading"""
    print("\nFetching playlist information...")
    videos = get_playlist_info(playlist_url)
    
    if not videos:
        print("Failed to fetch playlist information.")
        return
    
    print(f"\nFound {len(videos)} videos in playlist:\n")
    print("-" * 80)
    
    for i, video in enumerate(videos, 1):
        duration = video['duration']
        minutes = duration // 60
        seconds = duration % 60
        print(f"{i:3d}. {video['title']}")
        print(f"     URL: {video['url']} | Duration: {minutes}:{seconds:02d}")
        print()

def start_gui():
    """Launch GUI interface"""
    try:
        import tkinter as tk
        from tkinter import ttk, filedialog, messagebox, scrolledtext
    except ImportError:
        print("✗ tkinter not installed. GUI not available.")
        print("  Install with: pip install tk (or install python-tk on Linux)")
        return
    
    class DownloaderGUI:
        def __init__(self, root):
            self.root = root
            self.root.title("YouTube Downloader")
            self.root.geometry("700x600")
            
            # URL Input
            ttk.Label(root, text="YouTube URL:", font=('Arial', 10, 'bold')).pack(pady=(10, 5))
            self.url_entry = ttk.Entry(root, width=80)
            self.url_entry.pack(pady=5, padx=10)
            
            # Download Type
            type_frame = ttk.Frame(root)
            type_frame.pack(pady=10)
            ttk.Label(type_frame, text="Type:").pack(side=tk.LEFT, padx=5)
            self.download_type = tk.StringVar(value="single")
            ttk.Radiobutton(type_frame, text="Single Video", variable=self.download_type, 
                          value="single").pack(side=tk.LEFT, padx=5)
            ttk.Radiobutton(type_frame, text="Playlist", variable=self.download_type, 
                          value="playlist").pack(side=tk.LEFT, padx=5)
            
            # Quality Selection
            quality_frame = ttk.Frame(root)
            quality_frame.pack(pady=10)
            ttk.Label(quality_frame, text="Quality:").pack(side=tk.LEFT, padx=5)
            self.quality = tk.StringVar(value="best")
            qualities = ['best', '1080p', '720p', '480p', 'worst']
            ttk.Combobox(quality_frame, textvariable=self.quality, values=qualities, 
                        width=10, state='readonly').pack(side=tk.LEFT, padx=5)
            
            # Parallel Downloads (for playlists)
            parallel_frame = ttk.Frame(root)
            parallel_frame.pack(pady=10)
            self.use_parallel = tk.BooleanVar(value=False)
            ttk.Checkbutton(parallel_frame, text="Parallel Downloads", 
                          variable=self.use_parallel).pack(side=tk.LEFT, padx=5)
            ttk.Label(parallel_frame, text="Workers:").pack(side=tk.LEFT, padx=5)
            self.workers = tk.StringVar(value="3")
            ttk.Entry(parallel_frame, textvariable=self.workers, width=5).pack(side=tk.LEFT)
            
            # Video Range (for playlists)
            range_frame = ttk.Frame(root)
            range_frame.pack(pady=10)
            self.use_range = tk.BooleanVar(value=False)
            ttk.Checkbutton(range_frame, text="Video Range:", 
                          variable=self.use_range).pack(side=tk.LEFT, padx=5)
            ttk.Label(range_frame, text="From:").pack(side=tk.LEFT, padx=5)
            self.range_start = tk.StringVar(value="1")
            ttk.Entry(range_frame, textvariable=self.range_start, width=5).pack(side=tk.LEFT)
            ttk.Label(range_frame, text="To:").pack(side=tk.LEFT, padx=5)
            self.range_end = tk.StringVar(value="10")
            ttk.Entry(range_frame, textvariable=self.range_end, width=5).pack(side=tk.LEFT)
            
            # Output Directory
            dir_frame = ttk.Frame(root)
            dir_frame.pack(pady=10, fill=tk.X, padx=10)
            ttk.Label(dir_frame, text="Output:").pack(side=tk.LEFT, padx=5)
            self.output_dir = tk.StringVar(value="downloads")
            ttk.Entry(dir_frame, textvariable=self.output_dir, width=50).pack(side=tk.LEFT, 
                                                                              padx=5, fill=tk.X, expand=True)
            ttk.Button(dir_frame, text="Browse", command=self.browse_dir).pack(side=tk.LEFT)
            
            # Buttons
            button_frame = ttk.Frame(root)
            button_frame.pack(pady=10)
            ttk.Button(button_frame, text="Download", command=self.start_download, 
                      width=15).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="List Videos", command=self.list_videos, 
                      width=15).pack(side=tk.LEFT, padx=5)
            
            # Progress
            self.progress = ttk.Progressbar(root, mode='indeterminate')
            self.progress.pack(pady=10, padx=10, fill=tk.X)
            
            # Log Output
            ttk.Label(root, text="Log:", font=('Arial', 9, 'bold')).pack(pady=(5, 0))
            self.log_text = scrolledtext.ScrolledText(root, height=15, width=80, 
                                                     font=('Courier', 9))
            self.log_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
            
            self.downloading = False
        
        def log(self, message):
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.see(tk.END)
            self.root.update()
        
        def browse_dir(self):
            directory = filedialog.askdirectory()
            if directory:
                self.output_dir.set(directory)
        
        def list_videos(self):
            url = self.url_entry.get().strip()
            if not url:
                messagebox.showwarning("Warning", "Please enter a URL")
                return
            
            self.log_text.delete(1.0, tk.END)
            self.log("Fetching video information...")
            self.progress.start()
            
            def fetch():
                try:
                    videos = get_playlist_info(url)
                    self.progress.stop()
                    
                    if videos:
                        self.log(f"\nFound {len(videos)} videos:\n")
                        for i, video in enumerate(videos, 1):
                            duration = video['duration']
                            minutes = duration // 60
                            seconds = duration % 60
                            self.log(f"{i:3d}. {video['title']} ({minutes}:{seconds:02d})")
                    else:
                        self.log("Failed to fetch playlist information")
                except Exception as e:
                    self.progress.stop()
                    self.log(f"Error: {e}")
            
            threading.Thread(target=fetch, daemon=True).start()
        
        def start_download(self):
            if self.downloading:
                messagebox.showinfo("Info", "Download already in progress")
                return
            
            url = self.url_entry.get().strip()
            if not url:
                messagebox.showwarning("Warning", "Please enter a URL")
                return
            
            self.log_text.delete(1.0, tk.END)
            self.downloading = True
            self.progress.start()
            
            def download():
                try:
                    output_dir = self.output_dir.get()
                    quality = self.quality.get()
                    download_type = self.download_type.get()
                    
                    self.log(f"Starting download...")
                    self.log(f"URL: {url}")
                    self.log(f"Type: {download_type}")
                    self.log(f"Quality: {quality}")
                    self.log(f"Output: {Path(output_dir).absolute()}\n")
                    
                    if download_type == "single":
                        success = download_single_video(url, output_dir, quality)
                    else:
                        # Playlist download
                        video_range = None
                        if self.use_range.get():
                            try:
                                start = int(self.range_start.get())
                                end = int(self.range_end.get())
                                video_range = (start, end)
                                self.log(f"Range: videos {start}-{end}\n")
                            except ValueError:
                                self.log("Invalid range values, downloading all videos\n")
                        
                        if self.use_parallel.get():
                            try:
                                workers = int(self.workers.get())
                                workers = max(1, min(workers, 10))  # Limit between 1-10
                                self.log(f"Parallel workers: {workers}\n")
                            except ValueError:
                                workers = 3
                                self.log("Invalid worker count, using 3\n")
                            
                            success = download_playlist_parallel(url, output_dir, quality, 
                                                                workers, video_range)
                        else:
                            if video_range:
                                self.log("Note: Range selection with sequential download.\n")
                                self.log("Consider using parallel download for better performance.\n")
                            success = download_playlist(url, output_dir, quality)
                    
                    self.progress.stop()
                    self.downloading = False
                    
                    if success:
                        self.log("\n✓ All downloads completed successfully!")
                        messagebox.showinfo("Success", "Download completed!")
                    else:
                        self.log("\n✗ Download failed or incomplete")
                        messagebox.showwarning("Warning", "Download failed or incomplete")
                        
                except Exception as e:
                    self.progress.stop()
                    self.downloading = False
                    self.log(f"\nError: {e}")
                    messagebox.showerror("Error", f"Download error: {e}")
            
            threading.Thread(target=download, daemon=True).start()
    
    root = tk.Tk()
    app = DownloaderGUI(root)
    root.mainloop()

def main():
    """Main function"""
    print("=" * 50)
    print("YouTube Playlist Downloader - Enhanced")
    print("=" * 50)
    print()
    
    # Setup dependencies
    if not setup_dependencies():
        print("\nFailed to setup dependencies. Exiting.")
        return
    
    print()
    
    # Main menu
    print("Select mode:")
    print("1. Command Line Interface (CLI)")
    print("2. Graphical User Interface (GUI)")
    
    mode = input("\nEnter choice (1-2): ").strip()
    
    if mode == '2':
        start_gui()
        return
    
    # CLI Mode
    print("\n" + "=" * 50)
    
    # Get URL
    url = input("Enter YouTube URL (video or playlist): ").strip()
    
    if not url:
        print("No URL provided. Exiting.")
        return
    
    # Detect if it's a playlist
    is_playlist = 'playlist' in url.lower() or 'list=' in url
    
    if is_playlist:
        print("\n✓ Playlist detected")
        print("\nWhat would you like to do?")
        print("1. List all videos (no download)")
        print("2. Download entire playlist (sequential)")
        print("3. Download entire playlist (parallel - faster)")
        print("4. Download specific video range")
        print("5. Download with custom quality")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            list_playlist_videos(url)
        
        elif choice == '2':
            output_dir = input("\nEnter output directory (press Enter for 'downloads'): ").strip()
            if not output_dir:
                output_dir = 'downloads'
            print(f"Videos will be saved to: {Path(output_dir).absolute()}")
            download_playlist(url, output_dir)
        
        elif choice == '3':
            output_dir = input("\nEnter output directory (press Enter for 'downloads'): ").strip()
            if not output_dir:
                output_dir = 'downloads'
            
            workers = input("Number of parallel downloads (1-10, press Enter for 3): ").strip()
            try:
                workers = int(workers) if workers else 3
                workers = max(1, min(workers, 10))
            except ValueError:
                workers = 3
            
            print(f"\nVideos will be saved to: {Path(output_dir).absolute()}")
            print(f"Using {workers} parallel workers")
            download_playlist_parallel(url, output_dir, max_workers=workers)
        
        elif choice == '4':
            print("\nEnter video range to download:")
            try:
                start = int(input("  Start from video number: ").strip())
                end = int(input("  End at video number: ").strip())
                
                if start > end or start < 1:
                    print("Invalid range. Exiting.")
                    return
                
                output_dir = input("\nEnter output directory (press Enter for 'downloads'): ").strip()
                if not output_dir:
                    output_dir = 'downloads'
                
                use_parallel = input("Use parallel downloads? (y/n, press Enter for yes): ").strip().lower()
                
                if use_parallel != 'n':
                    workers = input("Number of parallel downloads (1-10, press Enter for 3): ").strip()
                    try:
                        workers = int(workers) if workers else 3
                        workers = max(1, min(workers, 10))
                    except ValueError:
                        workers = 3
                    
                    print(f"\nVideos will be saved to: {Path(output_dir).absolute()}")
                    download_playlist_parallel(url, output_dir, max_workers=workers, 
                                             video_range=(start, end))
                else:
                    print(f"\nVideos will be saved to: {Path(output_dir).absolute()}")
                    # For sequential with range, we need to modify the approach
                    print("\nNote: Sequential download doesn't support range selection yet.")
                    print("Using parallel download with 1 worker instead.")
                    download_playlist_parallel(url, output_dir, max_workers=1, 
                                             video_range=(start, end))
                    
            except ValueError:
                print("Invalid input. Exiting.")
                return
        
        elif choice == '5':
            print("\nAvailable qualities:")
            print("  best   - Best available quality")
            print("  1080p  - Full HD")
            print("  720p   - HD")
            print("  480p   - SD")
            print("  worst  - Lowest quality (smallest file)")
            
            quality = input("\nEnter quality (press Enter for 'best'): ").strip()
            if not quality:
                quality = 'best'
            
            output_dir = input("\nEnter output directory (press Enter for 'downloads'): ").strip()
            if not output_dir:
                output_dir = 'downloads'
            
            use_parallel = input("Use parallel downloads? (y/n, press Enter for yes): ").strip().lower()
            
            if use_parallel != 'n':
                workers = input("Number of parallel downloads (1-10, press Enter for 3): ").strip()
                try:
                    workers = int(workers) if workers else 3
                    workers = max(1, min(workers, 10))
                except ValueError:
                    workers = 3
                
                print(f"\nVideos will be saved to: {Path(output_dir).absolute()}")
                download_playlist_parallel(url, output_dir, quality, workers)
            else:
                print(f"\nVideos will be saved to: {Path(output_dir).absolute()}")
                download_playlist(url, output_dir, quality)
        
        else:
            print("Invalid choice. Exiting.")
    
    else:
        # Single video
        print("\n✓ Single video detected")
        print("\nAvailable qualities:")
        print("  best   - Best available quality")
        print("  1080p  - Full HD")
        print("  720p   - HD")
        print("  480p   - SD")
        print("  worst  - Lowest quality (smallest file)")
        
        quality = input("\nEnter quality (press Enter for 'best'): ").strip()
        if not quality:
            quality = 'best'
        
        output_dir = input("Enter output directory (press Enter for 'downloads'): ").strip()
        if not output_dir:
            output_dir = 'downloads'
        
        print(f"\nVideo will be saved to: {Path(output_dir).absolute()}")
        download_single_video(url, output_dir, quality)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)