from server.models import db, Event

def index(user_id):
    event = Event.query.filter(Event.user_id == user_id).all()
    return event


def insert(user_id:int, event:str, duration:float):
    event = Event(user_id=user_id, event=event, duration=duration)
    db.session.add(event)
    db.session.commit()
    return event

