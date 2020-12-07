from typing import Optional

from fastapi_camelcase import CamelModel


class CockpitSchema(CamelModel):
    # don't blame me, blame the devops for weird field naming
    idtask: Optional[int] = None
    name: Optional[str]
    version: Optional[int] = None
    reservedcredits: Optional[int] = None
    idapp: Optional[str] = None
    status: Optional[str] = "created"
    iduser: Optional[str] = None

    class Config:
        orm_mode = True

    def json(self):
        json_dict = {}
        for k, v in self.__dict__.items():
            capitalized = ''.join(word.title() for word in k.split('_'))
            json_dict[capitalized[0].lower() + capitalized[1:]] = v
        return json_dict