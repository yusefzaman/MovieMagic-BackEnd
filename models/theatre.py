from app import db

class Theatre(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    
    def __init__(self, id, name, location):
        self.id = id
        self.name = name
        

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            
        }
