import argparse
from karaoke_generator import KaraokeGenerator

def main():
    parser = argparse.ArgumentParser(description="Karaoke Video and SRT Generator")
    parser.add_argument("--lyrics", required=True, help="Path to the lyrics file")
    parser.add_argument("--song", required=True, help="Path to the song file")
    parser.add_argument("--image", required=True, help="Path to the background image file")
    parser.add_argument("--output", default="output", help="Output file prefix without extension")
    parser.add_argument("--offset", type=float, default=0.0, help="Offset in seconds to start the lyrics")
    parser.add_argument("--force-line-duration", type=float, help="Force a specific duration for each line")


    args = parser.parse_args()

    generator = KaraokeGenerator(args.lyrics, args.song, args.image, args.output, args.offset, args.force_line_duration)
    generator.generate()

if __name__ == "__main__":
    main()
