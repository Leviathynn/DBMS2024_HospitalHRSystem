from . import db

class historyItem(db.Model):
    number = db.Column(db.Integer, primary_key= True, autoincrement = True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    medicalCondition = db.Column(db.String(15))
    insuranceProvider = db.Column(db.String(20))
    estimatedCost = db.Column(db.String(20))
    
    def __repr__(self):
        breaks = "<br/> /n"
        return f"Inputs: Age({self.age}), Gender({self.gender}), Medical Condition({self.medicalCondition}), Insurance Provider({self.insuranceProvider}) --> Associated Predicted Cost - ${self.estimatedCost}\n"