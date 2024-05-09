from fastapi import APIRouter, status, HTTPException

from ..auth.dependencies import CurrentUser
from .dependencies import TaskRepo
from .schemas import NewTaskModel, TaskComment, Comment, TasksFilterRequest, TaskResponse, TaskStatus
from ...core import MESSAGE_OK
from ...exceptions import DBObjectNotFoundError


router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def new_task(task: NewTaskModel,
                   task_repo: TaskRepo,
                   _: CurrentUser):
    await task_repo.new_task(task)
    return MESSAGE_OK


@router.put("/status")
async def change_status(task: int, status: TaskStatus, task_repo: TaskRepo, _: CurrentUser):
    await task_repo.update_task_status(task, status)
    return MESSAGE_OK


@router.get("/available-filters")
async def available_filters(_: CurrentUser):
    return {
        "employee": {
            "description": "Id of employee",
            "type": "integer",
        },
        "name_substr": {
            "description": "Substring of task name",
            "type": "string",
        },
        "descr_substr": {
            "description": "Substring of task description",
            "type": "string",
        },
        "status": {
            "description": "Status of task",
            "type": "string",
            "values": {
                0: "backlog",
                1: "in progress",
                2: "review",
                3: "finished",
            }
        },
        "sprint": {
            "description": "Sprint id",
            "type": "integer",
        }
    }


@router.post("/filter", response_model=list[TaskResponse])
async def filter_tasks(task_repo: TaskRepo, filter_request: TasksFilterRequest, _: CurrentUser):
    return await task_repo.filter_tasks(filter_request)


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
