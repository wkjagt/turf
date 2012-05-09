import multiprocessing, socket, json
from event import Event

class Receiver(multiprocessing.Process):

    _master = None      # the master socket
    _event_queue = None  # the 
    _host = ()
    _buffer = 1024

    def __init__(self, event_queue, host):
        # construct the parent
        multiprocessing.Process.__init__(self)
        
        # set the values on the object
        self._event_queue = event_queue
        self._host = host
        
        # setup the socket that accepts events
        self._master = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._master.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._master.bind(self._host)
        

    def run(self):
        # start listening
        while True:
            data, addr = self._master.recvfrom(self._buffer)
            self._event_queue.put(Event(data))