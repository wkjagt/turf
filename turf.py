#! /usr/bin/python


import multiprocessing, glob, imp, sys, signal
from core.receiver import Receiver
from core.dispatcher import Dispatcher
from core.web import WebRequestHandler, WebServer
from core.plugin_mount import PluginContainer
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
    WEB_HOST = 'localhost'
    WEB_PORT = 8080


    # redis
    r = redis.StrictRedis(host = REDIS_HOST, port = REDIS_PORT, db = REDIS_DB)

    # import plugins in plugin folder
    import_plugins(PLUGIN_LOCATION)

    plugin_container = PluginContainer(r)



    # makes sure we can exit in a clean way
    signal.signal(signal.SIGINT, signal_handler)
    
    
    # the queue to which event objects are pushed
    eventQueue = multiprocessing.JoinableQueue()

    # the "server" (but actually a receiver)
    receiver = Receiver(eventQueue, (HOST, PORT))
    dispatcher = Dispatcher(eventQueue, r, plugin_container)

    receiver.start()
    dispatcher.start()

    # start the web server
    web_server = WebServer((WEB_HOST, WEB_PORT), WebRequestHandler)
    web_server.set_argument('plugin_container', plugin_container)

    web_server.serve_forever()


