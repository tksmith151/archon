from namespace.base import *

class Command:
    def __init__(self, string: str = None, *, quiet=False) -> None:
        self._string: str = string
        self._quiet: bool = quiet
        self._run()
        self.code = None
        self.stdout = None
        self.stderr = None
    
    def _run(self):
        self._show("Running:", self._string)
        all_out = []
        all_err = []
        with subprocess.Popen(shlex.split(self._string), stdin=sys.stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8') as process:
            while True:
                out = process.stdout.read(1)
                err = process.stderr.read(1)
                if out == "" and err == "" and process.poll() is not None:
                    break
                all_out.append(out)
                all_err.append(err)
                self._show(out, end="")
            self.code = process.wait()
            self.stdout = "".join(all_out)
            self.stderr = "".join(all_err)
            if self.stderr != "":
                print(self.stderr)
        self._show("Done!\n")

    def _show(self, text, end="\n"):
        if not self._quiet:
            print(text, end=end, flush=True)