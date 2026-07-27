"""
Test the Client class
"""

import pytest  # noqa: F401, F403

import bambulabs_api as bl
from bambulabs_api.printer_info import NozzleType
from bambulabs_api.states_info import GcodeState

mqtt = bl.PrinterMQTTClient(hostname="", access="", printer_serial="")
mqtt.manual_update(
    {
        "print": {
            "s_obj": [1, 2, 3],
            "nozzle_diameter": "0.4",
            "gcode_state": "FINISH",
            "nozzle_type": "hardened_steel",
        },
        "info": {
            "command": "get_version",
            "sequence_id": "",
            "module": [
                {
                    "name": "ota",
                    "sw_ver": "01.07.00.00",
                },
            ]
        }
    }
)


def test_get_skipped_objects():
    assert mqtt.get_skipped_objects() == [1, 2, 3]


def test_get_nozzle_type():
    assert mqtt.nozzle_type() == NozzleType.HARDENED_STEEL
    assert mqtt.nozzle_type() == "hardened_steel"
    assert str(mqtt.nozzle_type()) == "hardened_steel"


def test_get_state():
    assert mqtt.get_printer_state() == GcodeState.FINISH

    mqtt_ = bl.PrinterMQTTClient(hostname="", access="", printer_serial="")
    mqtt_.manual_update(
        {
            "print": {
                "gcode_state": "FAILED",
            },
        }
    )
    assert mqtt_.get_printer_state() == GcodeState.FAILED
    assert mqtt_.get_printer_state() == "FAILED"
    assert str(mqtt_.get_printer_state()) == "FAILED"


def test_nozzle_diameter():
    assert mqtt.nozzle_diameter() == 0.4


def test_get_firmware():
    assert mqtt.firmware_version() == "01.07.00.00"
    assert mqtt.printer_info.firmware_version == "01.07.00.00"


def test_incremental_update_preserves_sibling_fields():
    """A partial report must not wipe fields it does not mention."""
    mqtt_ = bl.PrinterMQTTClient(hostname="", access="", printer_serial="")
    mqtt_.manual_update(
        {
            "print": {
                "gcode_state": "RUNNING",
                "ams": {
                    "ams_exist_bits": "1",
                    "tray_exist_bits": "f",
                    "ams": [{"id": "0", "tray": [{"id": "0"}]}],
                },
            },
        }
    )
    # An incremental report mentioning only part of the ams object
    mqtt_.manual_update(
        {
            "print": {
                "ams": {
                    "ams": [{"id": "0", "tray": [{"id": "0", "tray_color": "FF0000FF"}]}],
                },
            },
        }
    )

    ams = mqtt_._data["print"]["ams"]  # noqa: SLF001
    assert ams["ams_exist_bits"] == "1", "sibling field dropped by partial update"
    assert ams["tray_exist_bits"] == "f", "sibling field dropped by partial update"
    assert ams["ams"][0]["tray"][0]["tray_color"] == "FF0000FF", "update not applied"
    assert mqtt_._data["print"]["gcode_state"] == "RUNNING"  # noqa: SLF001


def test_update_replaces_scalars_and_lists():
    """Lists and scalars are replaced, not merged."""
    mqtt_ = bl.PrinterMQTTClient(hostname="", access="", printer_serial="")
    mqtt_.manual_update({"print": {"gcode_state": "RUNNING", "s_obj": [1, 2]}})
    mqtt_.manual_update({"print": {"gcode_state": "FINISH", "s_obj": [9]}})
    assert mqtt_._data["print"]["gcode_state"] == "FINISH"  # noqa: SLF001
    assert mqtt_._data["print"]["s_obj"] == [9]  # noqa: SLF001
