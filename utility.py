import json
import shlex
import subprocess
from typing import List

def display_lines(lines: List[str]):
    for line in lines:
        print(line)

class Command:
    def __init__(self) -> None:
        self._description: List[str] = []
        self._string: str = None
        self._result = None

    def add(self, description: str):
        self._description.append(f"# {description}")

    def set(self, string: str):
        if not self._string:
            self._string = string
            return
        raise Exception("Cannot set a command string twice")

    def show_summary(self):
        display_lines(self._description)
        print(self._string)

    def run(self):
        if not self._result:
            result = subprocess.run(shlex.shlex(self._string), capture_output=True, text=True)
            self._result = result
            return
        raise Exception("Cannot run a command twice")
    
    @property
    def stdout(self):
        output: str = self._result.stdout.decode('utf-8')
        return output