from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Any

class SampleFormat(IntEnum):
    FLOAT32: SampleFormat

@dataclass
class DecodedSoundFile:
    samples: bytes
    nchannels: int
    sample_rate: int

def decode_file(path: str, *, output_format: SampleFormat = ...) -> DecodedSoundFile: ...
