from core.plugin_mount import EventHandler
from time import time

class RegistrationHandler(EventHandler):
    
    event_type = 'registration'
    
    pipe = None
    key = None
    
    def register_event(self):
        
        self.pipe = self._redis.pipeline()

        self.createKey()
        self.storeData()
        self.storeTags()
        self.storeSorted()

        self.pipe.execute()
        
    def createKey(self):
        self.key = '%s:%d' % (self.event.get_type(), self._redis.incr('registration.id'))
        
    def storeData(self):
        # make sure we also save a timestamp
        data = { 'timestamp' : int(time()) }
        data.update(self.event.get_data())
        self.pipe.hmset(self.key, data)
        
    def storeTags(self):
        for tag in self.event.get_tags():

            # add this event to the generic tag set
            self.pipe.sadd(tag, self.key)

            # add this event to the event having this tag set
            self.pipe.sadd('%s:%s' % (self.event.get_type(), tag), self.key)
    
    def storeSorted(self):
        self.pipe.zadd(self.event.get_type(), int(time()), self.key)


    def get_results(self, query):
        # get range
        start = self.iso_to_unix(query['start_date'].pop()) if 'start_date' in query else 0
        end = self.iso_to_unix(query['end_date'].pop()) if 'end_date' in query else 'inf'
        
        ids = self._redis.zrangebyscore('registration', start, end)
        
        registrations = []
        for id in ids:
            registrations.append(self._redis.hgetall(id))
        
        return registrations
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        