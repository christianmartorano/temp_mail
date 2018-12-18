try:
    import progressbar
except Exception as e:
    print('Necessário instalar pacote progressbar')

import time

def prog_bar_show(seg):
    for i in progressbar.progressbar(range(seg)):
        time.sleep(1)
