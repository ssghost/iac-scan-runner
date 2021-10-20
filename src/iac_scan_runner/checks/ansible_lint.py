from typing import Optional

import src.iac_scan_runner.vars as env
from pydantic import SecretStr
from src.iac_scan_runner.check import Check
from src.iac_scan_runner.check_output import CheckOutput
from src.iac_scan_runner.check_target_entity_type import CheckTargetEntityType
from src.iac_scan_runner.utils import run_command


class AnsibleLintCheck(Check):
    def __init__(self):
        super().__init__("ansible-lint", "Ansible Lint is a command-line tool for linting playbooks, roles and "
                                         "collections aimed towards any Ansible users", CheckTargetEntityType.iac)
        self.counter = 0

    def configure(self, config_filename: Optional[str], secret: Optional[SecretStr]) -> CheckOutput:
        if config_filename:
            self._config_filename = config_filename
            return CheckOutput(f'Check: {self.name} has been configured successfully.', 0)
        else:
            raise Exception(f'Check: {self.name} requires you to pass a configuration file.')

    def run(self, directory: str) -> CheckOutput:
        if self._config_filename:
            return run_command(f'ansible-lint -p -c {env.CONFIG_DIR}/{self._config_filename}', directory)
        else:
            return run_command("ansible-lint -p", directory)
