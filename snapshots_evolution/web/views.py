from fastapi import APIRouter

from domain.calculate_objects_evolutions_service import (
    CalculateObjectsEvolutionsService,
)
from web._utils import parse_dataclass_as
from web.serializers import (
    ObjectEvolutionsResponse,
    CalculateObjectsEvolutionsRequest,
)


router = APIRouter()


@router.post('/', response_model=list[ObjectEvolutionsResponse])
async def post(
    request: CalculateObjectsEvolutionsRequest
) -> list[ObjectEvolutionsResponse]:
    objects_evolutions = CalculateObjectsEvolutionsService().execute(
        snapshots=request.snapshots,
        key_field_name=request.key_field_name,
        datetime_field_name=request.datetime_field_name,
        exclude_fields_names=request.exclude_fields_names,
    )

    return parse_dataclass_as(
        list[ObjectEvolutionsResponse], objects_evolutions
    )
