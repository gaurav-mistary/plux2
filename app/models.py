from datetime import datetime
from app import app, login, db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login.user_loader
def user_loader(id):
    return User.query.get(int(id))

requests = db.Table(
    'requests',
    db.Column('sender_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('receiver_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30))
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password_hash = db.Column(db.String(130), nullable=False)
    about_me = db.Column(db.Text)
    profile_pic = db.Column(db.String(50), default='default.jpg')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    requested = db.relationship(
        'User',
        secondary=requests,
        primaryjoin=(requests.c.sender_id == id),
        secondaryjoin=(requests.c.receiver_id == id),
        backref = db.backref('requests', lazy='dynamic'),
        lazy='dynamic'
    )
    
    def __repr__(self):
        return f'<User: {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        token = s.dumps({'user_id': self.id}).decode('utf-8')
        return token
    
    @staticmethod
    def verify_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    
    def has_requested(self, user):
        return self.requested.filter(requests.c.receiver_id == user.id).count() > 0
    
    def request_from(self, user):
        return self.requests.filter(requests.c.sender_id == user.id).count() > 0 
    
    def send_request(self, user):
        if not self.has_requested(user):
            self.requested.append(user)
    
    def cancel_request(self, user):
        if self.has_requested(user):
            self.requested.remove(user)
    
            
    