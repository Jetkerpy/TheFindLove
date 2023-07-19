from django.conf import settings

# from django.contrib.sessions.models import Session
# Session.objects.all()
# aa =Session.objects.get(pk = "")

class HobbySession:
    def __init__(self, request) -> None:
        self.session = request.session
        hobbies = self.session.get(settings.HOBBY_SESSION_DATA)
        
        if not settings.HOBBY_SESSION_DATA in self.session:
            hobbies = self.session[settings.HOBBY_SESSION_DATA] = {}
        
        self.hobbies = hobbies

    
    def add(self, _ids):
        self.hobbies['hobby'] = _ids        
        self.save()

    
    def get_hobbies(self):
        return self.hobbies['hobby']
    

    def clear(self):
        del self.session[settings.HOBBY_SESSION_DATA]
        self.save()

        
    def save(self):
        """
        This method saved data in the session 
        """
        self.session.modified = True