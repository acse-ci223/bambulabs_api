from enum import Enum

NOZZLE_DIAMETER = {
    0.8,
    0.6,
    0.4,
    0.2,
}


class NozzleType(str, Enum):
    """
    Enum class for the nozzle type

    Attributes
    ----------
    STAINLESS_STEEL: The stainless steel nozzle type.
    HARDENED_STEEL: The hardened steel nozzle type.
    """
    STAINLESS_STEEL = "stainless_steel"
    HARDENED_STEEL = "hardened_steel"
