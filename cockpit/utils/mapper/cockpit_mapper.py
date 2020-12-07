from cockpit.model.cockpit_model import CockpitModel
from cockpit.schema.cockpit_schema import CockpitSchema


def cockpit_model_to_schema(cockpit_model: CockpitModel) -> CockpitSchema:
    return CockpitSchema(
        idtask=cockpit_model.id_task,
        name=cockpit_model.name,
        version=cockpit_model.version,
        reservedcredits=cockpit_model.reserved_credits,
        idapp=cockpit_model.id_app,
        status=cockpit_model.status,
        iduser=cockpit_model.id_user
    )