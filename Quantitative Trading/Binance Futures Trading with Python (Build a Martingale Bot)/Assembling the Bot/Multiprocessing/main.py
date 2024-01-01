from classes import Bot
from threading import Thread

bot1 = Bot("BTCUSDT",0.01,1,10,-0.05,1.2,7,2,"LONG",3)
bot2 = Bot("ETHUSDT",0.01,1,10,-0.05,1.2,7,2,"LONG",3)

def f1():
    bot1.run()
def f2():
    bot2.run()

t1 = Thread(target=f1)
t2 = Thread(target=f2)

t1.start()
t2.start()
