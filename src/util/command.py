from namespace.base import *

class Command:
    def __init__(self, string: str = None) -> None:
        self._string: str = string
        self._comments: List[str] = []
        self._result = None

    def comment(self, description: str):
        self._comments.append(f"# {description}")

    def show_summary(self):
        for line in self._comments:
            print(line)
        print(self._string)
        print()
    
    def run(self, show_progress=False):
        if not self._result:
            print("Running:", self._string)
            if show_progress:
                result = subprocess.run(shlex.split(self._string), stdin=sys.stdin ,stdout=sys.stdout, stderr=sys.stderr)
            else:
                result = subprocess.run(shlex.split(self._string), capture_output=True, text=True)
            self._result = result
            print("Done!\n")
            return self
        raise Exception("Cannot run a command twice")
    
    @property
    def stdout(self):
        if not self._result:
            raise Exception("Must run command first")
        output: str = self._result.stdout
        return output
    
    @property
    def stderr(self):
        if not self._result:
            raise Exception("Must run command first")
        output: str = self._result.stderr
        return output