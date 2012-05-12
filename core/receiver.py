import multiprocessing, socket, json
from event import Event

class Receiver(multiprocessing.Process):
    """
    Lightweigth class which sole purpose is to accept a UDP connection, and wait for incoming events.
    This runs in a separate process and should be as available as possible
    """

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
        """
        Start listening. When data comes in, instantiate an Event object with the received data
        and add it to th event queue. Let the other process handle validation, because we want to
        be ready to accept the next event data
        """
        while True:
            data, addr = self._master.recvfrom(self._buffer)
            self._event_queue.put(Event(data))