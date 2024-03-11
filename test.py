# import py7zr
# import pylzma

import subprocess
from easyZip import EasyZip
import envoy

# # url = "//192.168.123.3/藏经阁/bdyun/test2/新建文件夹/soul-ibm5100-4736-20231115.zip"
# url="//192.168.123.3/藏经阁/bdyun/test2/新建文件夹/1 (1).zip"
# out_url = "./xx"
# pw = "uohsoaixgnaixgnawab"

# # cmd = f'7z x "{url}" -o"{out_url}" -p"{pw}" -y'
# # print(cmd)
# # pipe=subprocess.run(cmd, shell=True,stdout=subprocess.PIPE,bufsize=1)

# o = EasyZip(url, out_url)
# o.extract("123")

# with py7zr.SevenZipFile(url, "r", password=pw) as ar:
#     ar.extractall(path=out_url)

# fp=open(url,"rb")
# ar=pylzma.Archive7z(fp,password=pw)
# pylzma.

# names=ar.getnames()
# print(names)

# cmd = "ping baidu.com"
# c = envoy.run(cmd)
# if c.std_out != None:
#     print(c.std_out)
# c = subprocess.Popen(
#     cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
# if c.stdout != None:
#     print(c.stdout.read())
a:str=""
if not a:
    print("true")
else:
    print("false")