import yt_dlp

def download_video():
    url = input("Enter the YouTube video URL: ").strip()
    if not url:
        print("Error: URL cannot be empty.")
        return
    
    quality = input("Enter the desired video quality (e.g., 360p, 480p, 720p, 1080p): ").strip()
    if not quality:
        print("Error: Quality cannot be empty.")
        return

    # Options for yt-dlp
    ydl_opts = {
        'format': f'bestvideo[height<={quality[:-1]}]+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',  # Ensures video and audio are merged if needed
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Attempting to download video in {quality} quality...")
            ydl.download([url])
            print("Download completed!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_video()
