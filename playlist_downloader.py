#!/usr/bin/env python3
"""
YouTube Playlist Downloader
Downloads all videos from a YouTube playlist using yt-dlp
Auto-installs dependencies (yt-dlp, ffmpeg) based on OS
"""

import subprocess
import sys
import json
import os
import platform
import zipfile
import shutil
from pathlib import Path
from urllib.request import urlretrieve

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

def download_playlist(playlist_url, output_dir='downloads', quality='best'):
    """
    Download all videos from a playlist
    
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
        '--restrict-filenames',
        playlist_url
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n" + "=" * 50)
        print("Download complete!")
        print("=" * 50)
    except subprocess.CalledProcessError as e:
        print(f"\nError during download: {e}")
        return False
    except KeyboardInterrupt:
        print("\n\nDownload interrupted by user")
        print("You can resume by running the script again with the same URL")
        return False
    
    return True

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

def main():
    """Main function"""
    print("=" * 50)
    print("YouTube Playlist Downloader")
    print("=" * 50)
    print()
    
    # Setup dependencies
    if not setup_dependencies():
        print("\nFailed to setup dependencies. Exiting.")
        return
    
    print()
    
    # Get playlist URL
    playlist_url = input("Enter YouTube playlist URL: ").strip()
    
    if not playlist_url:
        print("No URL provided. Exiting.")
        return
    
    # Menu
    print("\nWhat would you like to do?")
    print("1. List all videos (no download)")
    print("2. Download entire playlist")
    print("3. Download with custom quality")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        list_playlist_videos(playlist_url)
    
    elif choice == '2':
        print("\nNote: Videos will be saved in a folder in the current directory")
        output_dir = input("Enter output directory (press Enter for 'downloads'): ").strip()
        if not output_dir:
            output_dir = 'downloads'
        print(f"Videos will be saved to: {Path(output_dir).absolute()}")
        download_playlist(playlist_url, output_dir)
    
    elif choice == '3':
        print("\nAvailable qualities:")
        print("  best   - Best available quality")
        print("  1080p  - Full HD")
        print("  720p   - HD")
        print("  480p   - SD")
        print("  worst  - Lowest quality (smallest file)")
        
        quality = input("\nEnter quality (press Enter for 'best'): ").strip()
        if not quality:
            quality = 'best'
        
        print("\nNote: Videos will be saved in a folder in the current directory")
        output_dir = input("Enter output directory (press Enter for 'downloads'): ").strip()
        if not output_dir:
            output_dir = 'downloads'
        
        print(f"Videos will be saved to: {Path(output_dir).absolute()}")
        download_playlist(playlist_url, output_dir, quality)
    
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)