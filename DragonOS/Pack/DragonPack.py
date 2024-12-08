
def install(flag="-c"):
	match flag:
		case '-c':
			print('instaling DragonConsole')
		case _:
			print('not flag')
