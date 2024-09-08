from namespace.base import *

class Command:
    def __init__(self, string: str = None, *, quiet=False) -> None:
        self._string: str = string
        self._quiet: bool = quiet
        self.code = None
        self.stdout = None
        self.stderr = None
        self._run()
    
    def _run(self):
        self._show("Running:", self._string)
        all_out = []
        all_err = []
        with subprocess.Popen(shlex.split(self._string), stdin=sys.stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8') as process:
            while True:
                out = process.stdout.readline()
                err = process.stderr.readline()
                if out == "" and err == "" and process.poll() is not None:
                    break
                all_out.append(out)
                all_err.append(err)
                self._show(out, end="")
            self.code = process.wait()
        self.stdout = "".join(all_out)
        self.stderr = "".join(all_err)
        if self.stderr != "":
            if self.code != 0:
                print("ERROR!")
            else:
                print("Warning!")
            print(self.stderr)
            print()
        else:
            self._show("Success!\n")

    def _show(self, text, end="\n"):
        if not self._quiet:
            print(text, end=end, flush=True)