from home import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %id %r %r>' % (self.id, self.username, self.password)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(200))
    crtTime = db.Column(db.String(20))

    def __init__(self, userid, content, crtTime):
        self.userid = userid
        self.content = content
        self.crtTime = crtTime

    def __repr__(self):
        '<Post %r: %r [%r]' % (self.userid, self.content, self.crtTime)