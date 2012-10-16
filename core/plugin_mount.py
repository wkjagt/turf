from time import strptime, mktime

class PluginPasson(Exception):
    """
    Custom exception to let the dispatcher know that it hasn't yet found the correct plugin
    """
    
    def __init__(self, value = None):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
        




class PluginMount(type):
    """
    Meta class for event handles plugins
    """
    
    def __init__(cls, name, bases, attrs):
        """
        Create a list of plugin classes on the plugins attribute
        """
        if not hasattr(cls, 'plugins'):
            # going here means we're defining EventHandler itself. Set the plugins
            # attribute. After that, everything that extends it will have the plugins attribute
            # defined, so we can start adding the actual plugin class definitions to it
            cls.plugins = []
        else:
            # going here means we're defining a class that extends EventHandler
            cls.plugins.append(cls)




class EventHandler(object):

    """
    Extending classes must implement def register_event(self):
    
    Because this class defines PluginMount as its meta class, each definition of an extending
    plugin triggers __init__ on this meta class and adds the plugin to its plugin list.
    
    """
    __metaclass__ = PluginMount
    
    _redis = None
    
    def __init__(self, redis):

        self._redis = redis

    def set_event(self, event):

        """
        self.event_type needs to be defined in the plugin because the dispatcher loops through all the plugins
        to find the one that handles the event type that needs to be saved, we tell it to pass the event on to the next
        plugin if the event type is not the one that's defined in the plugin
        """
        try:
            if event.get_type() == self.event_type:
                # we give it the event, and the redis connection to save the event
                self.event = event
                return self
            else:
                # not our event type, continue
                raise PluginPasson
        except AttributeError:
            # event type not set, continue (if all the plugins are coded correctly,
            # this is the default plugin, but we can't be certain)
            raise PluginPasson
        
        
    def iso_to_unix(self, iso):
        if len(iso) == 19:
            struct = strptime(iso, '%Y-%m-%dT%H:%M:%S')
            return int(mktime(struct))
        
        
class PluginContainer(object):

    """
    Collection of instantiated plugins
    """

    _plugins = {}

    def __init__(self, redis):
        
        for plugin in EventHandler.plugins:
            self._plugins[plugin.event_type] = plugin(redis)

    def get(self, event_type):
        return self._plugins[event_type] if event_type in self._plugins else None

