from fastapi import APIRouter, status, HTTPException

from ..auth.dependencies import CurrentUser
from .dependencies import TaskRepo
from .schemas import NewTaskModel, TaskComment, Comment
from ...core import MESSAGE_OK
from ...exceptions import DBObjectNotFoundError


router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def new_task(task: NewTaskModel,
                   task_repo: TaskRepo,
                   _: CurrentUser):
    await task_repo.new_task(task)
    return MESSAGE_OK


@router.post("/filter")
async def filter_tasks(task_repo: TaskRepo, _: CurrentUser):
    # TODO: find comments
    pass


@router.get("/comment", response_model=list[Comment])
async def get_comments(task: int, task_repo: TaskRepo, _: CurrentUser):
    try:
        return await task_repo.task_comments(task)
    except DBObjectNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.post("/comment", status_code=status.HTTP_201_CREATED)
async def new_task_comment(comment: TaskComment, task_repo: TaskRepo, user: CurrentUser):
    await task_repo.leave_comment(comment, user.id)
    return MESSAGE_OK
