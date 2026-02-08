# mswin-sounddevice-audio-player

Play a sound file on a specific Windows audio output device by name.

Uses `sounddevice` (PortAudio) for device-targeted playback and `miniaudio` for decoding audio files.

Recommended: install via [wsl-sys-cli](https://github.com/jonathan-tyler/wsl-sys-cli) instead for WSL integration.

## Supported Formats

Any format supported by miniaudio: WAV, FLAC, MP3, and Vorbis.

## Installation

Install dependencies into Windows Python:

```powershell
python.exe -m pip install -r requirements.txt
```

### WSL Integration

Install [wsl-sys-cli](https://github.com/jonathan-tyler/wsl-sys-cli)

```bash
# Default device
sys play notify.mp3

# Windows audio device named "speakers"
sys play alert.mp3 --device speakers
```

### (Optional) Standalone

```powershell
# Default device
python.exe __main__.py --file ding.wav

# Windows audio device named "speakers"
python.exe __main__.py --file alert.wav --device speakers

# Windows audio device named "headphones"
python.exe __main__.py --file notify.wav --device headphones
```

## Development (WSL)

This sub-project is Windows-only at runtime, but you can still develop it from WSL.

- The Windows runtime dependencies in `requirements.txt` are guarded with environment markers, so in WSL they will be skipped.
- For editor type-checking in WSL (Pylance/Pyright), the repo provides local stub packages under `mswin/typings/`.

Recommended WSL setup:

```bash
# In your WSL virtualenv (or whatever Python you use for editing/tools)
python -m pip install -r requirements-wsl-dev.txt
```

Notes:

- If Pylance still shows unresolved imports after pulling changes, reload the VS Code window or restart the Pylance language server.
- To actually run the player, install dependencies into Windows Python and execute via `python.exe` as shown above.
