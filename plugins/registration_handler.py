from core.plugin_mount import EventHandler

class RegistrationHandler(EventHandler):
    
    event_type = 'registration'
    
    def register_event(self):
        print self.event