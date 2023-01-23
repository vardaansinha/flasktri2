from sqlalchemy import Column, Integer, String, Boolean
from __init__ import db
import random


class Subscription(db.Model):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    _username = Column(String(255), nullable=False)
    _premium = Column(Boolean, nullable=False)

    def __init__(self, username, premium=False):
        self._username = username
        self._premium = premium

    def __repr__(self):
        return "<Subscription(id='%s', username='%s', premium='%s')>" % (
            self.id,
            self.username,
            self.premium,
        )

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def premium(self):
        return self._premium

    @premium.setter
    def premium(self, value):
        self._premium = value

    def to_dict(self):
        return {"id": self.id, "username": self.username, "premium": self.premium}


def init_subscriptions():
    s1 = Subscription("vardsin28")
    s2 = Subscription("navanyatavelli")
    s3 = Subscription("ShauryaGoel")
    s4 = Subscription("JustinN")
    s5 = Subscription("JakeF")
    s6 = Subscription("SYeung")
    s7 = Subscription("JMort")

    subscriptions = [s1, s2, s3, s4, s5, s6, s7]
   
    for sub in subscriptions:
        # randomly assign premium subscriptions to users
        premium = bool(random.getrandbits(1))
        sub.premium = premium

        try:
            db.session.add(sub)
            db.session.commit()
        except Exception as e:
            print("error while creating subscription: " + str(e))
            db.session.rollback()
