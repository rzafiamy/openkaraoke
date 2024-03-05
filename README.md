# Karaoke Video and SRT Generator

## Description
This script generates a karaoke video from a given song, lyrics, and a background image. It automatically times the lyrics with the song's duration and outputs an MP4 video file and an SRT subtitle file.

## Setup
- Ensure you have Python 3.6+ installed.
- Install the required packages: `pip install -r requirements.txt`
```bash
sudo apt-get install imagemagick
```
## Usage
- Run the script with the following command:
```bash
python manager.py --lyrics path/to/lyrics.txt --song path/to/song.mp3 --image path/to/background.jpg --output output_prefix
```

Replace path/to/lyrics.txt, path/to/song.mp3, and path/to/background.jpg with the paths to your lyrics file, song file, and background image, respectively. output_prefix will be used to name the output files.

## Output

    The script will generate two files:
        An MP4 video file (output_prefix.mp4) with the karaoke video.
        An SRT subtitle file (output_prefix.srt) with the timed lyrics.


### Explanation

- **MoviePy**: Handles video editing tasks such as combining audio, image, and text clips.
- **SRT Library**: For generating the SRT file with correctly timed subtitles.
- **TextClip**: Creates text overlays for each line of lyrics.
- **AudioFileClip & ImageClip**: Used to load the song and background image.
- **CompositeVideoClip**: Combines multiple clips into a single video output.
- **Config**: Externalizes configuration to avoid hardcoding values, making the script more flexible.

