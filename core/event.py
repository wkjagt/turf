import multiprocessing, socket, json

class Event(object):
    
    _event_type = None
    _event_tags = []
    _event_data = None
    
    def __init__(self, message):
        try:
            decoded = json.loads(message)
            self._event_type = decoded['event']
            self._event_tags = decoded['tags'] if 'tags' in decoded else []
            self._event_data = decoded['data'] if 'data' in decoded else {}

        except (ValueError, KeyError):
            pass
        
    def get_type(self):
        return self._event_type

    def get_tags(self):
        return self._event_tags

    def get_data(self):
        return self._event_data


    def __str__(self):
        return self._event_type