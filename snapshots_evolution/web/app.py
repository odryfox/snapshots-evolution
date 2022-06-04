from fastapi import FastAPI

from domain.calculate_objects_evolutions_service import (
    CalculateObjectsEvolutionsService,
)

app = FastAPI()


@app.get('/')
async def get():
    res = CalculateObjectsEvolutionsService().execute(
        snapshots=[],
        key_field_name='',
        datetime_field_name='',
        exclude_fields_names=[],
    )
    return {'res': res}
