from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip
from config import Config
import datetime
from PIL import Image, ImageDraw, ImageFont


class KaraokeGenerator:
    def __init__(self, lyrics_path, song_path, image_path, output_prefix, offset=0.0, force_line_duration=None):
        self.lyrics_path = lyrics_path
        self.song_path = song_path
        self.image_path = image_path
        self.output_prefix = output_prefix
        self.offset = offset
        self.force_line_duration = force_line_duration

    def generate(self):
        song = AudioFileClip(self.song_path)

        duration = song.duration

        with open(self.lyrics_path, 'r') as file:
            lyrics_lines = file.read().splitlines()

        if self.force_line_duration:
            duration_per_line = self.force_line_duration
        else:
            duration_per_line = (duration - self.offset) / len(lyrics_lines)

        background = ImageClip(self.image_path).set_duration(duration).set_audio(song)

        subtitles = []
        clips = [background]
        for index, line in enumerate(lyrics_lines):
            start_time = self.offset + index * duration_per_line
            end_time = (index + 1) * duration_per_line
            subtitles.append(self.format_srt_entry(index + 1, start_time, end_time, line))

            # Create an image with text for this line
            text_image_path = f"{Config.OUTPUT_DIR}/temp_text_{index}.png"
            # self.create_text_image(line, text_image_path, duration_per_line)
            prev_line = lyrics_lines[index - 1] if index > 0 else ""
            next_line = lyrics_lines[index + 1] if index < len(lyrics_lines) - 1 else ""
            self.create_text_image2(prev_line, line, next_line, text_image_path, size=(800, 150))

            text_clip = ImageClip(text_image_path).set_duration(duration_per_line).set_start(start_time).set_position("center", "bottom")
            clips.append(text_clip)

        with open(f"{Config.OUTPUT_DIR}/{self.output_prefix}.srt", "w") as srt_file:
            srt_file.write("\n\n".join(subtitles))

        final_clip = CompositeVideoClip(clips)
        final_clip.write_videofile(f"{Config.OUTPUT_DIR}/{self.output_prefix}.mp4", fps=24)

    def format_srt_entry(self, index, start, end, content):
        start_srt = str(datetime.timedelta(seconds=round(start))).replace(".", ",")
        end_srt = str(datetime.timedelta(seconds=round(end))).replace(".", ",")
        return f"{index}\n{start_srt} --> {end_srt}\n{content}"

    def create_text_image(self, text, filename, duration, size=(800, 50), background_color=(0, 0, 0), font_color=(255, 255, 255)):
        """Creates an image with the given text."""
        # image = Image.new('RGBA', size, (255, 255, 255, 0))  # Last value 0 indicates fully transparent
        image = Image.new('RGB', size, color=background_color)
        font_path = Config.FONT_PATH  # Ensure this path is correct in config.py
        font_size = 24
        font = ImageFont.truetype(font_path, font_size)
        draw = ImageDraw.Draw(image)
        textwidth, textheight = self.__textsize(text, font)

        # Center the text
        x = (size[0] - textwidth) / 2
        y = (size[1] - textheight) / 2
        draw.text((x, y), text, fill=font_color, font=font)

        image.save(filename)

    def create_text_image2(self, prev_line, current_line, next_line, filename, size=(800, 150), background_color=(0, 0, 0), current_font_color=(255, 255, 255), other_font_color=(128, 128, 128)):
        """Creates an image with previous, current, and next text lines."""
        image = Image.new('RGB', size, color=background_color)
        font_path = Config.FONT_PATH
        font_size_current = 24
        font_size_other = 20
        font_current = ImageFont.truetype(font_path, font_size_current)
        font_other = ImageFont.truetype(font_path, font_size_other)
        draw = ImageDraw.Draw(image)

        # Calculate text size and positions
        width_current, height_current = self.__textsize(current_line, font_current)
        width_prev, height_prev = self.__textsize(prev_line, font_other)
        width_next, height_next = self.__textsize(next_line, font_other)

        # Draw previous line
        x_prev = (size[0] - width_prev) / 2
        y_prev = (size[1] / 3 - height_prev) / 2
        draw.text((x_prev, y_prev), prev_line, fill=other_font_color, font=font_other)

        # Draw current line
        x_current = (size[0] - width_current) / 2
        y_current = size[1] / 3 + (size[1] / 3 - height_current) / 2
        draw.text((x_current, y_current), current_line, fill=current_font_color, font=font_current)

        # Draw next line
        x_next = (size[0] - width_next) / 2
        y_next = 2 * size[1] / 3 + (size[1] / 3 - height_next) / 2
        draw.text((x_next, y_next), next_line, fill=other_font_color, font=font_other)

        image.save(filename)


    def __textsize(self, text, font):
        im = Image.new(mode="P", size=(0, 0))
        draw = ImageDraw.Draw(im)
        _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
        return width, height

    