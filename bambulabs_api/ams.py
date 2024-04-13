from enum import Enum, auto
from bambulabs_api.filament_info import FilamentTray


class AMS:
    def __init__(self, humidity: str, temperature: float) -> None:
        self.filament_trays: dict[int, FilamentTray] = {}

        self.humidity = humidity
        self.temperature = temperature

    def set_filament_tray(self,
                          filament_tray: FilamentTray,
                          tray_index: int) -> None:
        self.filament_trays[tray_index] = filament_tray

    def get_filament_tray(self, tray_index: int) -> FilamentTray | None:
        return self.filament_trays.get(tray_index)


class Humidity(Enum):
    LEVEL_0 = auto()
    LEVEL_1 = auto()
    LEVEL_2 = auto()
    LEVEL_3 = auto()
    LEVEL_4 = auto()
    LEVEL_5 = auto()
