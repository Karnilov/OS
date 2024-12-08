from comm import git
from main import run
def install(flag="-c"):
	text=open('run.py').read()
	if not 'import kivy' in text:
		text='import kivy\n'+text
	open('run.py', "w").write(text)
	match flag:
		case '-c':
			git('https://github.com/Karnilov/OS/blob/main/DragonOS/Console/install')
			run('install/install.comm')
		case '-c':
			git('https://github.com/Karnilov/OS/blob/main/DragonOS/OS/install')
			run('install/install.comm')
		case _:
			print("Err index")
