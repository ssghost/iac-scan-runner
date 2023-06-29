from typing import Optional

from pydantic import SecretStr
import iac_scan_runner.vars as env
from iac_scan_runner.interface.check import Check
from iac_scan_runner.functionality.check_output import CheckOutput
from iac_scan_runner.enums.check_target_entity_type import CheckTargetEntityType
from iac_scan_runner.utils import run_command


class ClocCheck(Check):
    """Clock class object."""

    def __init__(self):
        super().__init__("cloc", "Counts blank lines, comment lines, and physical lines of source code in many "
                                 "programming languages", CheckTargetEntityType.IAC)
        self._config_filename = None

    def configure(self, config_filename: Optional[str],
                  secret: Optional[SecretStr]) -> CheckOutput:  # pylint: disable=unused-argument
        """Set configuration."""
        if config_filename:
            self._config_filename = config_filename
            return CheckOutput(f"Check: {self.name} has been configured successfully.", 0)
        raise Exception(f"Check: {self.name} requires you to pass a configuration file.")

    def run(self, directory: str) -> CheckOutput:
        """Run check."""
        if self._config_filename:
            return run_command(f"{env.CLOC_CHECK_PATH} --config {env.CONFIG_DIR}/{self._config_filename} .", directory)
        return run_command(f"{env.CLOC_CHECK_PATH} .", directory)
