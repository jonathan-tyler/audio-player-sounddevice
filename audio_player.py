from __future__ import annotations

import sys
from pathlib import Path
from typing import cast

import miniaudio
import numpy as np
import sounddevice as sd


class AudioPlayer:

    def play(self, file_path: str, device_name: str | None = None) -> None:
        path = Path(file_path)
        if not path.is_file():
            print(f"File not found: {file_path}")
            sys.exit(1)

        device_index: int | None = None
        if device_name is not None:
            device_index = self.__resolve_device(device_name)
            if device_index is None:
                sys.exit(1)

        data, samplerate = self.__read_audio(path)

        # Pad with 200 ms of silence so the last real samples flush
        # through the audio pipeline before the stream closes.
        silence_frames = int(samplerate * 0.2)
        if data.ndim == 1:
            padding = np.zeros(silence_frames, dtype=data.dtype)
        else:
            padding = np.zeros((silence_frames, data.shape[1]), dtype=data.dtype)
        data = np.concatenate([data, padding])

        sd.play(data, samplerate, device=device_index)
        sd.wait()

    @staticmethod
    def __read_audio(path: Path) -> tuple[np.ndarray, int]:
        """Decode audio via miniaudio (built-in MP3/FLAC/WAV support)."""
        decoded = miniaudio.decode_file(
            str(path),
            output_format=cast(
                miniaudio.SampleFormat,
                miniaudio.SampleFormat.FLOAT32,
            ),
        )
        samples = np.frombuffer(decoded.samples, dtype=np.float32)
        if decoded.nchannels > 1:
            samples = samples.reshape(-1, decoded.nchannels)
        return samples, decoded.sample_rate

    def __resolve_device(self, name: str) -> int | None:
        query = name.strip().lower()
        devices = sd.query_devices()

        if isinstance(devices, dict):
            devices = [devices]

        output_devices: list[tuple[int, str, str]] = []
        for i, dev in enumerate(devices):
            if dev["max_output_channels"] > 0:
                friendly = dev["name"]
                friendly_base = friendly.split("(")[0].strip()
                output_devices.append((i, friendly_base.lower(), friendly))

        # 1) Exact, case-insensitive match on the base name.
        for idx, norm, _friendly in output_devices:
            if norm == query:
                return idx

        # 2) Substring match.
        partial = [(idx, friendly) for idx, norm, friendly in output_devices if query in norm]
        if len(partial) == 1:
            return partial[0][0]

        if len(partial) > 1:
            print(f"Multiple devices matched '{name}'. Be more specific. Candidates:")
            for _idx, friendly in partial:
                print(f"  - {friendly}")
            return None

        print(f"No output device matched '{name}'. Available devices:")
        for _idx, _norm, friendly in output_devices:
            print(f"  - {friendly}")
        return None
