import re
import yt_dlp

def sanitize_filename(filename):
    """
    Sanitize the filename to remove invalid characters for file systems.
    """
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_video():
    url = input("Enter the YouTube video URL: ").strip()
    if not url:
        print("Error: URL cannot be empty.")
        return
    
    quality = input("Enter the desired video quality (e.g., 360p, 480p, 720p, 1080p): ").strip()
    if not quality:
        print("Error: Quality cannot be empty.")
        return

    # Directory where files will be saved (update as needed)
    output_directory = "C:/Users/user/Desktop/DownloadedVideos/"

    # Options for yt-dlp
    ydl_opts = {
        'format': f'bestvideo[height<={quality[:-1]}]+bestaudio/best',
        'outtmpl': f'{output_directory}%(title)s.%(ext)s',  # Use output directory
        'merge_output_format': 'mp4',  # Ensures video and audio are merged if needed
        'windowsfilenames': True,      # Adjust for Windows-specific filename rules
    }

    try:
        print(f"Attempting to download video in {quality} quality...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download completed!")
    except Exception as e:
        # Sanitize error messages if filename is an issue
        if "unable to open for writing" in str(e):
            print("Error: Filename contains invalid characters. Trying with sanitized filename...")
            ydl_opts['outtmpl'] = f'{output_directory}{sanitize_filename("%(title)s")}.%(ext)s'
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                print("Download completed with sanitized filename!")
            except Exception as e_inner:
                print(f"An error occurred during retry: {e_inner}")
        else:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_video()
