import os
import re
import yt_dlp


def sanitize_filename(filename):
    """
    Sanitize the filename by removing invalid characters and truncating it if too long.
    """
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)  # Remove invalid characters
    return sanitized[:100]  # Limit to 100 characters


def download_video():
    url = input("Enter the video URL: ").strip()
    if not url:
        print("Error: URL cannot be empty.")
        return

    quality = input("Enter the desired video quality (e.g., 360p, 480p, 720p, 1080p): ").strip()
    if not quality:
        print("Error: Quality cannot be empty.")
        return

    # Define output directory
    output_directory = os.path.join(os.getcwd(), "DownloadedVideos")
    os.makedirs(output_directory, exist_ok=True)  # Create directory if it doesn't exist

    # yt-dlp options
    ydl_opts = {
        'format': f'bestvideo[height<={quality[:-1]}]+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': False,
        'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
    }

    try:
        print(f"Attempting to download video in {quality} quality...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video info to get the title
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'downloaded_video')
            sanitized_title = sanitize_filename(video_title)

            # Update output template with sanitized filename
            ydl_opts['outtmpl'] = os.path.join(output_directory, f"{sanitized_title}.%(ext)s")

            # Reinitialize YoutubeDL with updated options
            with yt_dlp.YoutubeDL(ydl_opts) as ydl_sanitized:
                ydl_sanitized.download([url])
        print("Download completed!")
    except Exception as e:
        print(f"An error occurred: {e}")

        # Retry with a simple fallback filename if filename-related error
        if "unable to open for writing" in str(e):
            print("Filename issue detected. Retrying with a fixed filename...")
            fallback_filename = os.path.join(output_directory, 'downloaded_video.mp4')
            ydl_opts['outtmpl'] = fallback_filename
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl_retry:
                    ydl_retry.download([url])
                print("Download completed with fixed filename!")
            except Exception as retry_error:
                print(f"An error occurred during retry: {retry_error}")


if __name__ == "__main__":
    download_video()
