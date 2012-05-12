import multiprocessing
import plugin_mount

class Dispatcher(multiprocessing.Process):

    """
    Runs in a separate process from the receiver. The slightly heavier lifting is done here
    because we're less in a hurry.
    """
    _event_queue = None
    _redis = None
    
    def __init__(self, event_queue, redis):
        multiprocessing.Process.__init__(self)
        self._event_queue = event_queue
        self._redis = redis

    def run(self):
        """
        Wait for new events to be passed in the queue and pass it on to the registered plugin.
        
        """
        while True:
            # an event was passed to the queue by the receiver. 
            next_event = self._event_queue.get()

            # loop through the plugin classes and try to instantiate it with the event. If that throws
            # an exception, try with the next. Don't create a reference to it, so each unused plugin will
            # be garbage collected
            for plugin in plugin_mount.EventHandler.plugins:
                try:
                    plugin(next_event, self._redis).register_event()
                except plugin_mount.PluginPasson:
                    pass
            
            # consider the task done, because the plugin is done registering it
            self._event_queue.task_done()