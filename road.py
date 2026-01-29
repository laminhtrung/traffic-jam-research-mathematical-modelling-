from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Segment:
    kind: str        # "N" or "S"
    length: float
    vmax: float

class Road:
    def __init__(self, segments: List[Segment]):
        assert len(segments) > 0
        self.segments = segments
        self.L = sum(s.length for s in segments)

        # precompute boundaries for fast masking
        self.bounds: List[Tuple[float, float, str, float]] = []
        pos = 0.0
        for seg in segments:
            start = pos
            end = pos + seg.length
            self.bounds.append((start, end, seg.kind, seg.vmax))
            pos = end

    def length(self) -> float:
        return self.L
