from datetime import datetime

from pony.orm import Database, db_session
from pony.orm.core import ObjectNotFound, Optional, PrimaryKey, Required, desc

db = Database()


class BotUser(db.Entity):
    id = PrimaryKey(int)
    username = Optional(str)
    first_name = Required(str)
    last_name = Optional(str)
    created_at = Required(datetime, default=datetime.utcnow())
    updated_at = Required(datetime, default=datetime.utcnow())

    @property
    def full_name(self):
        return ('%s %s' % (self.first_name, self.last_name)).strip()

    @property
    def mention(self):
        if self.username:
            return '@%s' % self.username

    def __str__(self):
        return self.full_name

    @db_session
    def from_user(user):
        try:
            u = BotUser[user.id]
            u.updated_at = datetime.utcnow()
        except ObjectNotFound:
            u = BotUser(
                id=user.id,
                username=user.username or '',
                first_name=user.first_name,
                last_name=user.last_name or '',
            )
        return u

    @classmethod
    @db_session
    def count(cls):
        return cls.select().count()

    @classmethod
    @db_session
    def last_created(cls):
        return cls.select().order_by(lambda u: desc(u.created_at)).first()


db.bind(provider='sqlite', filename='db.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
