import yt_dlp
import re
import logging
import os
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FFmpeg configuration
FFMPEG_DIR = os.path.join(os.path.dirname(__file__), 'ffmpeg')
FFMPEG_PATH = os.path.join(FFMPEG_DIR, 'ffmpeg.exe')
FFPROBE_PATH = os.path.join(FFMPEG_DIR, 'ffprobe.exe')

def check_ffmpeg():
    """Verify FFmpeg binaries exist"""
    if not all(os.path.isfile(p) for p in [FFMPEG_PATH, FFPROBE_PATH]):
        print(f"""
        Error: FFmpeg binaries not found!
        Place these files in the 'ffmpeg' folder:
        - ffmpeg.exe
        - ffprobe.exe
        
        Current search path: {FFMPEG_DIR}
        """)
        return False
    return True

def sanitize_filename(filename):
    """Sanitize filename to prevent filesystem issues"""
    return re.sub(r'[\\/*?:"<>|]', "", filename).strip()

def get_user_choice(options, prompt):
    """Get user selection from a list of options"""
    print(prompt)
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")

def get_available_heights(formats):
    """Extract available video heights/qualities"""
    return sorted(
        {f.get('height') for f in formats if f.get('vcodec') != 'none' and f.get('height')},
        reverse=True
    )

def get_audio_languages(formats):
    """Extract available audio languages with their display names"""
    languages = {}
    for f in formats:
        if f.get('acodec') != 'none':
            lang_code = f.get('language') or 'und'
            lang_name = f.get('language_display') or lang_code
            languages[lang_code] = lang_name
    return languages

def convert_audio_to_aac(input_path):
    """Convert video file's audio to AAC using FFmpeg"""
    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_converted.mp4"

    command = [
        FFMPEG_PATH,
        '-i', input_path,
        '-c:v', 'copy',      # copy video stream
        '-c:a', 'aac',       # convert audio to AAC
        '-b:a', '192k',      # audio bitrate
        '-movflags', '+faststart',  # for web streaming
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Audio converted and saved to: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg conversion failed: {e}")
        return None

    return output_path

def main():
    """Main application flow"""
    if not check_ffmpeg():
        return
    
    url = input("Enter YouTube video URL: ").strip()
    if not re.search(r'(youtube\.com|youtu\.be)', url):
        print("Invalid YouTube URL.")
        return

    try:
        # Get video metadata
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
    except Exception as e:
        logger.error(f"Error fetching video info: {e}")
        return

    dl_type = get_user_choice(['MP3', 'MP4'], "Choose download type:")
    title = sanitize_filename(info['title'])
    base_ydl_opts = {
        'ffmpeg_location': FFMPEG_PATH,
        'ffprobe_location': FFPROBE_PATH,
        'outtmpl': f"{title}.%(ext)s",
    }

    if dl_type == 'MP3':
        ydl_opts = {
            **base_ydl_opts,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        heights = get_available_heights(formats)
        if not heights:
            print("No video formats available")
            return
        selected_height = get_user_choice(heights, "Select video quality:")

        audio_langs = get_audio_languages(formats)
        lang_options = ['Best available'] + list(audio_langs.values())
        selected_lang = get_user_choice(lang_options, "Select audio language:")

        format_spec = f'bestvideo[height={selected_height}]+bestaudio'
        if selected_lang != 'Best available':
            lang_code = [k for k, v in audio_langs.items() if v == selected_lang][0]
            format_spec += f'[language={lang_code}]'
        format_spec += '/bestvideo+bestaudio/best'

        ydl_opts = {
            **base_ydl_opts,
            'format': format_spec,
            'merge_output_format': 'mp4',
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download completed.")

        if dl_type == 'MP4':
            original_file = f"{title}.mp4"
            convert_audio_to_aac(original_file)

    except Exception as e:
        logger.error(f"Download failed: {e}")

if __name__ == '__main__':
    main()
