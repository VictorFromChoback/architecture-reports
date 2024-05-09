from datetime import datetime

from sqlalchemy import insert, select, update

from ...core import BaseRepository
from .orm import Tasks, TaskComments, task_comments
from ..auth.orm import employees
from .schemas import NewTaskModel, TaskStatus, TaskComment, Comment, TasksFilterRequest


class TaskRepository(BaseRepository):

    async def new_task(self, task: NewTaskModel):
        current_time = datetime.now()
        status = TaskStatus.BACKLOG if task.sprint is None else TaskStatus.INPROGRESS
        await self.execute(insert(Tasks).values(name=task.name,
                                                description=task.description,
                                                creation_datetime=current_time,
                                                change_datetime=current_time,
                                                employee=task.employee,
                                                sprint=task.sprint,
                                                status=status))

    async def leave_comment(self, comment_data: TaskComment, author: int):
        await self.execute(insert(TaskComments).values(task=comment_data.task,
                                                       author=author,
                                                       text=comment_data.comment,
                                                       creation_date=datetime.now()))

    async def task_comments(self, task: int) -> list[Comment]:
        data = await self.fetch_all(select(task_comments.join(employees,
                                                              task_comments.c.author == employees.c.id)))
        return [Comment(author=value["username"],
                        text=value["text"],
                        creation_date=value["creation_date"]) for value in data]

    async def update_task_status(self, task_id: int, status: TaskStatus) -> None:
        await self.execute(update(Tasks).where(Tasks.id == task_id).values(status=status))

    def _make_conds(self,
                    employee: int | None,
                    name_substr: str | None,
                    descr_substr: str | None,
                    status: TaskStatus | None,
                    sprint: int | None):
        conds = []
        if employee:
            conds.append(Tasks.employee == employee)
        if name_substr:
            conds.append(Tasks.name.like(f"%{name_substr}%"))
        if descr_substr:
            conds.append(Tasks.description.like(f"%{descr_substr}%"))
        if status:
            conds.append(Tasks.status == status)
        if sprint:
            conds.append(Tasks.sprint == sprint)
        return conds

    async def filter_tasks(self, request: TasksFilterRequest):
        return await self.fetch_objects(select(Tasks)
                                        .where(*self._make_conds(employee=request.employee,
                                                                 name_substr=request.name_substr,
                                                                 descr_substr=request.descr_substr,
                                                                 status=request.status,
                                                                 sprint=request.sprint)))
