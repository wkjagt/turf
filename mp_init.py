#! /usr/bin/python

import multiprocessing, glob, imp, sys, signal
from core.receiver import Receiver
from core.dispatcher import Dispatcher
from os.path import join, basename, splitext



def import_plugins(directory):
    modules = {}
    for path in glob.glob(join(directory,'[!_]*.py')):
        name, ext = splitext(basename(path))
        modules[name] = imp.load_source(name, path)

def signal_handler(signal, frame):
    sys.exit(0)

if __name__ == '__main__':

    # config
    HOST = 'localhost'
    PORT = 9900
    PLUGIN_LOCATION = 'plugins'

    # makes sure we can exit in a clean way
    signal.signal(signal.SIGINT, signal_handler)
    import_plugins(PLUGIN_LOCATION)

    eventQueue = multiprocessing.JoinableQueue()
    receiver = Receiver(eventQueue, ('localhost', 9900))
    dispatcher = Dispatcher(eventQueue)

    receiver.start()
    dispatcher.start()
