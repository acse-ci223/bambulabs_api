from bambulabs_api.filament_info import FilamentTray


class AMS:
    """
    Represents the Bambulab's AMS (Automated Material System) system.
    """
    def __init__(self, humidity: str, temperature: float) -> None:
        self.filament_trays: dict[int, FilamentTray] = {}

        self.humidity = humidity
        self.temperature = temperature

    def set_filament_tray(self,
                          filament_tray: FilamentTray,
                          tray_index: int) -> None:
        """
        Set the filament tray at the given index. Will overwrite any existing
        tray at the given index.

        Args:
            filament_tray (FilamentTray): description of the filament tray
            tray_index (int): tray index
        """
        self.filament_trays[tray_index] = filament_tray

    def get_filament_tray(self, tray_index: int) -> FilamentTray | None:
        """
        Get the filament tray at the given index. If no tray exists at the
        index, return None.

        Args:
            tray_index (int): tray index of the filament tray

        Returns:
            FilamentTray | None: filament tray at the given index
        """
        return self.filament_trays.get(tray_index)
