from cockpit.model.cockpit_model import CockpitModel
from cockpit.schema.cockpit_schema import CockpitSchema


def cockpit_model_to_schema(cockpit_model: CockpitModel) -> CockpitSchema:
    return CockpitSchema(
        id_task=cockpit_model.id_task,
        name=cockpit_model.name,
        version=cockpit_model.version,
        reserved_credits=cockpit_model.reserved_credits,
        id_app=cockpit_model.id_app,
        status=cockpit_model.status,
        priority=str(cockpit_model.priority),
        id_user=cockpit_model.id_user
    )