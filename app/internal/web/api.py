from http import HTTPStatus

from fastapi.routing import APIRouter
from scintillant.apimodels import SkillRequest, SkillResponse

from app.external.exceptions import ExceptionResponse
from app.internal.drivers.picklecache import PickleDBCache
from app.internal.logic.states.basic import ScenarioManager

general_router = APIRouter(responses={
    400: {'model': ExceptionResponse},
    500: {'model': ExceptionResponse}
})

skill_api = APIRouter(prefix='/skill')


@skill_api.post('/', response_model=SkillResponse)
async def skill(request: SkillRequest):
    user_context = PickleDBCache.get_or_create(f"{request.message.user.idx}_context")
    request.context = user_context
    manager = ScenarioManager(request)
    response = manager.get_response()
    PickleDBCache.update(f"{request.message.user.idx}_context", response.context)
    return response


general_router.include_router(skill_api)
