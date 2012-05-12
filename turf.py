#! /usr/bin/python


import multiprocessing, glob, imp, sys, signal
from core.receiver import Receiver
from core.dispatcher import Dispatcher
from os.path import join, basename, splitext
import redis



def import_plugins(directory):
    modules = {}
    for path in glob.glob(join(directory,'[!_]*.py')):
        name, ext = splitext(basename(path))
        modules[name] = imp.load_source(name, path)

def signal_handler(signal, frame):
    sys.exit(0)

if __name__ == '__main__':

    # config
    # todo, move to config file
    HOST = 'localhost'
    PORT = 9900
    PLUGIN_LOCATION = 'plugins'
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0


    # redis
    r = redis.StrictRedis(host = REDIS_HOST, port = REDIS_PORT, db = REDIS_DB)
    


    # makes sure we can exit in a clean way
    signal.signal(signal.SIGINT, signal_handler)
    
    # import plugins in plugin folder
    import_plugins(PLUGIN_LOCATION)

    # the queue to which event objects are pushed
    eventQueue = multiprocessing.JoinableQueue()

    # the "server" (but actually a receiver)
    receiver = Receiver(eventQueue, (HOST, PORT))
    dispatcher = Dispatcher(eventQueue, r)

    receiver.start()
    dispatcher.start()
