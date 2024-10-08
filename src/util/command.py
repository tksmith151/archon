from namespace.base import *

class Command:
    def __init__(self, string: str = None, *, quiet=False, capture=True, supress=False) -> None:
        self._string: str = string
        self._quiet: bool = quiet
        self._capture: bool = capture
        self._supress: bool = supress
        self.code = None
        self.stdout = None
        self.stderr = None
        self._run()
    
    def _run(self):
        self._show(f"Running: {self._string}")
        if not self._capture:
            result = subprocess.run(shlex.split(self._string), stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
            self.code = result.returncode
            self._check_code()
            return
        all_out = []
        all_err = []
        out = ""
        err = ""
        with subprocess.Popen(shlex.split(self._string), stdin=sys.stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8') as process:
            while True:
                while out != "":
                    self._show(out, end="")
                    all_out.append(out)
                    out = process.stdout.read(1)   
                while err != "":
                    self._show(err, end="")
                    all_err.append(err)
                    err = process.stderr.read(1)
                out = process.stdout.read(1)
                err = process.stderr.read(1)
                if out == "" and err == "" and process.poll() is not None:
                    break
            self.code = process.wait()
        self.stdout = "".join(all_out)
        self.stderr = "".join(all_err)
        if self.stderr != "":
            if self.code != 0:
                self._error("ERROR!")
            else:
                self._error("Warning!")
            self._error(self.stderr)
            self._error()
        else:
            self._show("Success!\n")
        self._check_code()

    def _show(self, text="", end="\n"):
        if not self._quiet:
            print(text, end=end, flush=True)

    def _error(self, text="", end="\n"):
        if not self._supress:
            print(text, end=end, flush=True)

    def _check_code(self):
        if self.code != 0 and not self._supress:
            raise Exception(F"Failed!")