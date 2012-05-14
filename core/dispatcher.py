import multiprocessing
import plugin_mount

class Dispatcher(multiprocessing.Process):

    """
    Runs in a separate process from the receiver. The slightly heavier lifting is done here
    because we're less in a hurry.
    """
    _event_queue = None
    _redis = None
    _plugin_container = None

    def __init__(self, event_queue, redis, plugin_container):
        multiprocessing.Process.__init__(self)
        self._event_queue = event_queue
        self._redis = redis
        self._plugin_container = plugin_container


    def run(self):
        """
        Wait for new events to be passed in the queue and pass it on to the registered plugin.
        
        """
        while True:
            # an event was passed to the queue by the receiver. 
            next_event = self._event_queue.get()


            plugin = self._plugin_container.get(next_event.get_type())

            if plugin is not None:
                plugin.set_event(next_event).register_event()
            
            # consider the task done, because the plugin is done registering it
            self._event_queue.task_done()