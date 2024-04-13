from dataclasses import dataclass
from enum import Enum
from typing import Any

__all__ = ["AMSFilamentSettings", "Filament"]


@dataclass(frozen=True)
class AMSFilamentSettings:
    """
    Dataclass for the filament settings

    The filament settings are a set of values that indicate the settings of the filament.

    Attributes
    ----------

    tray_info_idx: The tray info index.
    nozzle_temp_min: The minimum nozzle temperature.
    nozzle_temp_max: The maximum nozzle temperature.
    tray_type: The tray type.
    """  # noqa
    tray_info_idx: str
    nozzle_temp_min: int
    nozzle_temp_max: int
    tray_type: str


class Filament(AMSFilamentSettings, Enum):
    """
    Enum class for the filament settings

    The filament settings are a set of values that indicate the settings of the filament.

    Attributes
    ----------

    POLYLITE_PLA: The Polylite PLA filament settings.
    POLYTERRA_PLA: The Polyterra PLA filament settings.
    BAMBU_ABS: The Bambu ABS filament settings.
    BAMBU_PA_CF: The Bambu PA-CF filament settings.
    BAMBU_PC: The Bambu PC filament settings.
    BAMBU_PLA_Basic: The Bambu PLA Basic filament settings.
    BAMBU_PLA_Matte: The Bambu PLA Matte filament settings.
    SUPPORT_G: The Support G filament settings.
    SUPPORT_W: The Support W filament settings.
    BAMBU_TPU_95A: The Bambu TPU 95A filament settings.
    ABS: The ABS filament settings.
    ASA: The ASA filament settings.
    PA: The PA filament settings.
    PA_CF: The PA-CF filament settings.
    PC: The PC filament settings.
    PETG: The PETG filament settings.
    PLA: The PLA filament settings.
    PLA_CF: The PLA-CF filament settings.
    PVA: The PVA filament settings.
    TPU: The TPU filament settings.
    """  # noqa
    POLYLITE_PLA = "GFL00", 190, 250, "PLA"
    POLYTERRA_PLA = "GFL01", 190, 250, "PLA"
    BAMBU_ABS = "GFB00", 240, 270, "ABS"
    BAMBU_PA_CF = "GFN03", 270, 300, "PA-CF"
    BAMBU_PC = "GFC00", 260, 280, "PC"
    BAMBU_PLA_Basic = "GFA00", 190, 250, "PLA"
    BAMBU_PLA_Matte = "GFA01", 190, 250, "PLA"
    SUPPORT_G = "GFS01", 190, 250, "PA-S"
    SUPPORT_W = "GFS00", 190, 250, "PLA-S"
    BAMBU_TPU_95A = "GFU01", 200, 250, "TPU"

    ABS = "GFB99", 240, 270, "ABS"
    ASA = "GFB98", 240, 270, "ASA"
    PA = "GFN99", 270, 300, "PA"
    PA_CF = "GFN98", 270, 300, "PA"
    PC = "GFC99", 260, 280, "PC"
    PETG = "GFG99", 220, 260, "PETG"
    PLA = "GFL99", 190, 250, "PLA"
    PLA_CF = "GFL98", 190, 250, "PLA"
    PVA = "GFS99", 190, 250, "PVA"
    TPU = "GFU99", 200, 250, "TPU"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for filament in cls:
                if value == filament.name:
                    return filament

        raise ValueError(f"Filament {value} not found")


@dataclass
class FilamentTray:
    k: float
    n: int
    tag_uid: str
    tray_id_name: str
    tray_info_idx: str
    tray_type: str
    tray_sub_brands: str
    tray_color: str
    tray_weight: str
    tray_diameter: str
    tray_temp: str
    tray_time: str
    bed_temp_type: str
    bed_temp: str
    nozzle_temp_max: int
    nozzle_temp_min: int
    xcam_info: str
    tray_uuid: str

    @staticmethod
    def keys():
        return FilamentTray.__dataclass_fields__.keys()

    @staticmethod
    def from_dict(d: dict[str, Any]):
        keys = set(FilamentTray.keys())
        d = {k: v for k, v in d.items() if k in keys}

        return FilamentTray(**d)

    def filament(self) -> Filament:
        return Filament(
            self.tray_info_idx,
            self.nozzle_temp_min,
            self.nozzle_temp_max,
            self.tray_type
            )
