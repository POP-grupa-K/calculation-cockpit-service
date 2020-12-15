from typing import Optional

from fastapi_camelcase import CamelModel


class CockpitSchema(CamelModel):
    # don't blame me, blame the devops for weird field naming
    id_task: Optional[int] = None
    name: str
    version: Optional[int] = None
    reserved_credits: int
    id_app: int
    status: Optional[str] = "created"
    priority: Optional[str] = "1"
    id_user: int

    class Config:
        orm_mode = True

    def json(self):
        json_dict = {}
        for k, v in self.__dict__.items():
            capitalized = ''.join(word.title() for word in k.split('_'))
            json_dict[capitalized[0].lower() + capitalized[1:]] = v
        return json_dict