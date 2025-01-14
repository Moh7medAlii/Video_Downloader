import yt_dlp

# Define a callback function to show progress
def progress_hook(d):
    if d['status'] == 'downloading':
        print(
            f"\rDownloading: {d['_percent_str']} | "
            f"Speed: {d['_speed_str']} | "
            f"ETA: {d['_eta_str']} | "
            f"Size: {d['_total_bytes_str']}",
            end=""
        )
    elif d['status'] == 'finished':
        print("\nDownload complete. Finalizing...")

# Prompt the user to input the video or playlist URL
video_url = input("Please enter the video or playlist URL: ").strip()

# Prompt the user to choose the desired quality
print("\nChoose the desired quality:")
print("1. 1080p (FHD)")
print("2. 720p (HD)")
print("3. 480p (SD)")
print("4. 360p (Low)")
print("5. 240p (Very Low)")
print("6. Best available up to 1080p")
print("7. MP3 (Audio Only - High Quality)")
quality_choice = input("Enter your choice (1-7): ").strip()

# Map the user's choice to the format string
quality_formats = {
    "1": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "2": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "3": "bestvideo[height<=480]+bestaudio/best[height<=480]",
    "4": "bestvideo[height<=360]+bestaudio/best[height<=360]",
    "5": "bestvideo[height<=240]+bestaudio/best[height<=240]",
    "6": "(bestvideo[height<=1080]+bestaudio/best[height<=1080])/best",
    "7": "bestaudio/best",  # Audio-only download
}
download_format = quality_formats.get(quality_choice, quality_formats["6"])  # Default to "Best available up to 1080p"

# Set output options
if quality_choice == "7":  # MP3 format
    ydl_opts = {
        'format': download_format,
        'outtmpl': '%(title)s.%(ext)s',  # Save file with video title
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',  # High-quality MP3 (192kbps)
        }],
        'noplaylist': False,  # Allow playlists for MP3
        'progress_hooks': [progress_hook],  # Add progress display
    }
else:
    ydl_opts = {
        'format': download_format,
        'outtmpl': '%(playlist_title)s/%(title)s.%(ext)s',  # Save in a folder named after the playlist
        'merge_output_format': 'mp4',  # Merge audio and video into an MP4 file
        'noplaylist': False,  # Allow downloading playlists
        'progress_hooks': [progress_hook],  # Add progress display
    }

# Download the video or playlist
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print("\nThe download has been completed successfully!")
except Exception as e:
    print(f"\nAn error occurred: {e}")
