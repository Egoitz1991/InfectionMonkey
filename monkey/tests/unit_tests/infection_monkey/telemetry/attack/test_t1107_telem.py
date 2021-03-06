import json
from pathlib import Path

import pytest

from common.utils.attack_utils import ScanStatus
from infection_monkey.telemetry.attack.t1107_telem import T1107Telem

# Convert to path to fix path separators for current os
PATH = str(Path("path/to/file.txt"))
STATUS = ScanStatus.USED


@pytest.fixture
def T1107_telem_test_instance():
    return T1107Telem(STATUS, PATH)


def test_T1107_send(T1107_telem_test_instance, spy_send_telemetry):
    T1107_telem_test_instance.send()
    expected_data = {"status": STATUS.value, "technique": "T1107", "path": PATH}
    expected_data = json.dumps(expected_data, cls=T1107_telem_test_instance.json_encoder)
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == "attack"


def test_T1107_send__path(spy_send_telemetry):
    T1107Telem(STATUS, Path(PATH)).send()
    assert json.loads(spy_send_telemetry.data)["path"] == PATH
