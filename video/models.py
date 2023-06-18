import datetime
import ormar
from db import MainMeta
from user.models import User
from typing import Optional, Union, Dict


class Video(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=50)
    description: str = ormar.String(max_length=500)
    file: str = ormar.String(max_length=1000)
    file_type: str = ormar.String(max_length=100)
    create_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    user: Optional[Union[User, Dict]] = ormar.ForeignKey(User)

