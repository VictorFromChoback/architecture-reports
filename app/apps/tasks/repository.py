from datetime import datetime

from sqlalchemy import insert, select

from ...core import BaseRepository
from .orm import Tasks, TaskComments, task_comments
from ..auth.orm import employees
from .schemas import NewTaskModel, TaskStatus, TaskComment, Comment


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
