from fastapi import APIRouter, Depends

from dependencies import verify_token

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)


@router.get("/")
def read_agents():
    return [
        {"id": 1, "name": "Search Agent"},
        {"id": 2, "name": "Summary Agent"},
    ]


@router.post(
    "/run",
    dependencies=[Depends(verify_token)],
)
def run_agent(prompt: str):
    return {
        "prompt": prompt,
        "result": f"Agent response for: {prompt}",
    }
