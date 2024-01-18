from abc import ABC
from sk_fx.indicators.idtypes import TimeFrame


class Oscillator(ABC):
    name: str
    time_frame: TimeFrame

    def __init__(self, name: str, time_frame: TimeFrame) -> None:
        super(Oscillator, self).__init__()
        self.name = name
        self.time_frame = time_frame

    def __str__(self):
        print(f"Oscillator {self.name.title()} - {self.time_frame}")
