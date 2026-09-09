from fastapi import APIRouter

router = APIRouter(
    # 프리픽스 지정 가능
    prefix="/users",
    tags=["users"],
)


@router.get("/")
def read_users():
    return [
        {"id": 1, "name": "Kim"},
        {"id": 2, "name": "Lee"},
    ]


@router.get("/{user_id}")
def read_user(user_id: int):
    return {
        "id": user_id,
        "name": "Kim",
    }
