import multiprocessing, socket, json

class Event(object):
    
    _event_type = None
    _event_data = None
    
    def __init__(self, message):
        try:
            decoded = json.loads(message)
            self._event_type, self._event_data = decoded['event_type'], \
                        decoded['event_data'] if 'event_data' in decoded else None

        except (ValueError, KeyError):
            pass
        
    def get_type(self):
        return self._event_type

    def __str__(self):
        return self._event_type