import subprocess
from typing import Callable, NoReturn, Any


class EasyZip():

    def __init__(self, url: str, out: str, exeurl: str = '7z') -> None:
        self.url = url
        self.out = out
        self.exeurl = exeurl
        self.cmd = ''
        pass

    def extract_cmd(self, pw: str | None = None) -> subprocess.Popen[bytes] | None:
        if pw is None:
            self.cmd = f'{self.exeurl} x "{self.url}" -o"{self.out}" -aoa -y'
        else:
            self.cmd = f'{self.exeurl} x "{self.url}" -o"{self.out}" -aoa -p"{pw}"  -y'
        # self.cmd="ping www.baidu.com"
        print(self.cmd)
        return subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def extract(self,
                pw: str | None = None,
                cb: Callable[[subprocess.Popen[str] | None], Any] | None = None):
        subp = self.extract_cmd(pw)
        if subp == None:
            return
        while subp.poll() is None:
            stdout = subp.stdout

            if stdout != None:
                line = stdout.readline()
                line = line.strip()
                if line:
                    print(line.decode())
            stderr = subp.stderr
            if stderr != None:
                line = stderr.readline()
                line = line.strip()
                if line:
                    print("err:"+line.decode())
        print(subp.returncode)
        if subp.returncode == 0:
            print('subp success')
        else:
            print('subp failed')
        pass
