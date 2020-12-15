from typing import Optional

from fastapi_camelcase import CamelModel


class UserAppSchema(CamelModel):
    id_app: int
    id_user: int

    class Config:
        orm_mode = True

    def json(self):
        json_dict = {}
        for k, v in self.__dict__.items():
            capitalized = ''.join(word.title() for word in k.split('_'))
            json_dict[capitalized[0].lower() + capitalized[1:]] = v
        return json_dict