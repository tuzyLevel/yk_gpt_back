from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.user import get_user_by_id
from app.db.database import get_db
from .schema import RequestPostCheckUser, ResponsePostCheckUser, UserSchema
from app.core.swagger_auth import get_current_username


user_router = APIRouter(
    tags=["User"],
)


@user_router.post("", dependencies=[Depends(get_current_username)])
async def request_check_user(
    req: RequestPostCheckUser,
    db: Session = Depends(get_db),
) -> ResponsePostCheckUser:
    user_info = get_user_by_id(req.id, db=db)
    if user_info is not None:
        return ResponsePostCheckUser(
            existed=True, data=UserSchema.model_validate(user_info)
        )
    else:
        return ResponsePostCheckUser(existed=False)
