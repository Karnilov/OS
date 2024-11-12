import classes.core
import threading 
import importlib
import settings.core as settings 
cores=classes.core.core()
scc=threading.Thread(target=classes.core.scc(cores).regulation,daemon=True)
scc.start()
def getCpu():
    max=0
    print('\u001b[38;5;15m'+"_" * ((65)))
    print('|core 0 |core 1 |core 2 |core 3 |core 4 |core 5 |core 6 |core 7 |')
    for item in cores.cores:
        if len(item)>max:max=len(item)
    if max>0:
        print('\u001b[38;5;15m'+"_" * ((65)))
        txt='|'
        for q ,i in enumerate(cores.cores):
            if not 'asyncio' in settings.cores['8'][q]:
                if len(i)>0:
                    txt+=(str(int(i[0].load()))+'%    ')[:7]+'|'
                else:
                    txt+='0%     |'
            else:
                txt+='   -   |'
        print(txt)
        print('\u001b[38;5;15m'+"_" * ((65)))
    for i in range(max):
        try:
            core1=(cores.cores[0][i].name+'       ')[:7]
        except:
            core1='   -   '
        try:
            core2=(cores.cores[1][i].name+'       ')[:7]
        except:
            core2='   -   '
        try:
            core3=(cores.cores[2][i].name+'       ')[:7]
        except:
            core3='   -   '
        try:
            core4=(cores.cores[3][i].name+'       ')[:7]
        except:
            core4='   -   '
        try:
            core5=(cores.cores[4][i].name+'       ')[:7]
        except:
            core5='   -   '
        try:
            core6=(str(cores.cores[5][i].name)+'       ')[:7]
        except:
            core6='   -   '
        try:
            core7=(cores.cores[6][i].name+'       ')[:7]
        except:
            core7='   -   '
        try:
            core8=(cores.cores[7][i].name+'       ')[:7]
        except:
            core8='   -   '
        print('|'+core1+'|'+core2+'|'+core3+'|'+core4+'|'+core5+'|'+core6+'|'+core7+'|'+core8+'|')
    print("_" * ((65)))
def addProcces(name):
    globals()[name+'App']=importlib.import_module("home."+name)
    application=globals()[name+'App'].app()
    application.start()
    cores.add_process(application, application.type)
