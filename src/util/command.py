from namespace.base import *

class Command:
    def __init__(self, string: str = None, *, quiet=False) -> None:
        self._string: str = string
        self._run()
        self.stdout = None
        self.stderr = None
    
    def _run(self):
        print("Running:", self._string)
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
                print(out, end="", flush=True)
        self.stdout = "".join(all_out)
        self.stderr = "".join(all_err)
        if self.stderr != "":
            print(self.stderr)
        print("Done!\n")