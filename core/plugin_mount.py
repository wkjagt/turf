class PluginPasson(Exception):
    
    def __init__(self, value = None):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
        

class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            cls.plugins.append(cls)

class EventHandler(object):

    """
    Extending classes must implement
    def register_event(self):
    """
    __metaclass__ = PluginMount
    
    def __init__(self, event):
        # check if it's the proper event type
        
        try:
            if event.get_type() == self.event_type:
                self.event = event
            else:
                raise PluginPasson
        except AttributeError:
            raise PluginPasson
        
        
        
        