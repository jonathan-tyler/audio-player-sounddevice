from __future__ import annotations

from argparse import ArgumentParser, Namespace

try:
    from .audio_player import AudioPlayer
# Allows running this file directly as a script.
except ImportError:
    from audio_player import AudioPlayer


def register_args(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to the sound file to play.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        help="Name of the output device (e.g. 'speakers', 'headphones'). Uses system default if omitted.",
    )


def run(args: Namespace) -> None:
    player = AudioPlayer()
    player.play(args.file, args.device)


if __name__ == "__main__":
    parser = ArgumentParser(description="Sound file player with device targeting")
    register_args(parser)
    run(parser.parse_args())
