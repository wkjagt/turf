import multiprocessing
import plugin_mount

class Dispatcher(multiprocessing.Process):

    _event_queue = None
    
    def __init__(self, event_queue):
        multiprocessing.Process.__init__(self)
        self._event_queue = event_queue

    def run(self):
        """
        Wait for new events to be passed in the queue
        and pass it on to the registered plugin
        """
        while True:
            next_event = self._event_queue.get()

            if next_event is None:
                self._event_queue.task_done()
                break

            for plugin in plugin_mount.EventHandler.plugins:
                try:
                    plugin(next_event).register_event()
                except plugin_mount.PluginPasson:
                    pass
                
            self._event_queue.task_done()