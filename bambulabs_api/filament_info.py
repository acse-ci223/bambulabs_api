from dataclasses import dataclass
from enum import Enum

__all__ = ["AMSFilamentSettings", "Filament"]


@dataclass(frozen=True)
class AMSFilamentSettings:
    tray_info_idx: str
    nozzle_temp_min: int
    nozzle_temp_max: int
    tray_type: str


class Filament(AMSFilamentSettings, Enum):
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
