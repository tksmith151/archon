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
        print()

    def confirm(self):
        confirmed = False
        self.show_summary()
        confirmed = input("Perform above command (y/N):")
        if confirmed == "y":
            self.run()
            print(self.stderr)
            print(self.stdout)
            print()
            return confirmed
        print()
        return confirmed



    def run(self):
        if not self._result:
            result = subprocess.run(shlex.split(self._string), capture_output=True, text=True)
            self._result = result
            return
        raise Exception("Cannot run a command twice")
    
    @property
    def stdout(self):
        output: str = self._result.stdout
        return output
    
    @property
    def stderr(self):
        output: str = self._result.stderr
        return output