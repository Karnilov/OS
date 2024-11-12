import os
library=['request']
dir=['adding','home','classes','settings','adding/comm','home/auto']
file={
'main.py':'''from comm import *
import threading
import time
import os
connectLib=[]
graphicMode=False
def comm(commands):
    if commands=='': return None
    cmd=commands.split('\n')
    for command in cmd:
        print("[38;5;10mfor[38;5;220m<<"+str(command))
        args=command.split(" ")
        func=args[0]
        del args[0]
        try:
            eval(func+"(*"+str(args)+")")
        except Exception as exc:
            print("[38;5;1m"+str(exc)+"[38;5;15m")
def run(path):
    path='home/'+path
    file = open(path).read()
    for cmd in file.split('\n'):
        eval(path.split('.')[-1]+'("'+cmd+'")')
def connect(link):
    connectLib.append(link)
def reload():
    for f in os.listdir("adding/comm/"):
        name=f.split(".")[0]
        print("[38;5;11madding.comm."+name+"...",end='')
        try:
            globals()[name]=importlib.import_module("adding.comm."+name)
            print('[38;5;10mLOAD')
        except:
            print('[38;5;1mERROR')
    for f in connectLib:
        print("[38;5;11m"+f+"...",end='')
        try:
            globals()[f.split('/')[-1]]=importlib.import_module(f)
            print('[38;5;10mLOAD')
        except:
            print('[38;5;1mERROR')
    for f in os.listdir("home/auto/"):
        print('runing:'+f)
        run('auto/'+f)
reload()
if not graphicMode:
    while True:
        try:
            comm(input("[38;5;12m>>[38;5;15m"))
        except EOFError:
            pass''',
'comm.py':'''import urllib.parse
import sys
import requests
import os
import importlib
def colors():
    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            sys.stdout.write(u"[38;5;" + code + "m " + code.ljust(4))
        print(u"[0m")
def download_file(file_url, folder_path):
    response = requests.get(file_url)
    filename = os.path.join(folder_path, file_url.split('/')[-1])
    with open(filename, 'wb') as f:
        f.write(response.content)
        print(f'[38;5;11mСкачан файл: {filename}')
def download_folder_contents(folder_url, folder_path):
    response = requests.get(folder_url)
    if response.status_code == 200:
        contents = response.json()
        os.makedirs(folder_path, exist_ok=True)
        for item in contents:
            if item['type'] == 'file':
                download_file(item['download_url'], folder_path)
            elif item['type'] == 'dir':
                new_folder_path = os.path.join(folder_path, item['name'])
                download_folder_contents(item['url'], new_folder_path)
    else:
        print(f'Ошибка при получении содержимого папки: статус код {response.status_code}')
def getUrl(link):
    lk=link.split('/')
    for q in range(3):
        del lk[0]
    owner=lk[0]
    del lk[0]
    repo=lk[0]
    del lk[0]
    for q in range(2):
        del lk[0]
    path='/'.join(lk)
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    return url
def ls():
    print(os.listdir())
def git(link, *args):
    if '-a' in args:
        download_folder_contents(getUrl(link), link.split("/")[len(link.split("/"))-1])
        print("[38;5;10mDone")
    else:
        if '-f'in args:
            download_file(getUrl(link), 'home/')
            print("[38;5;10mDone")
        else:
            download_folder_contents(getUrl(link), 'home/'+link.split("/")[len(link.split("/"))-1])
            print("[38;5;10mDone")''',
'run.py':"""import main"""
}
for q in dir:
    print("\u001b[38;5;11mcreating direction:"+q+"...",end='')
    os.mkdir(q)
    print("\u001b[38;5;10mDone")
for name, text in file.items():
    print("\u001b[38;5;11minstalling:"+str(name)+"...",end='')
    with open(name,'w') as f:
        f.write(text)
    print("\u001b[38;5;10mDone")
for q in library:
    print("\u001b[38;5;11minstalling library:"+q+"...")
    os.system('pip install '+q)
    print("\u001b[38;5;10mDone")
