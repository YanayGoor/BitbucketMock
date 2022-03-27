from typing import Optional, Literal, TypeVar, Generic, List, Any

from pydantic import BaseModel


T = TypeVar("T")


PRState = Literal["ALL", "OPEN", "DECLINED", "MERGED"]


class Project(BaseModel):
    key: str


class Repo(BaseModel):
    slug: str
    name: Optional[str]
    project: Project


class Ref(BaseModel):
    id: str
    repository: Repo


class NewPullRequest(BaseModel):
    title: str
    description: str
    fromRef: Ref
    toRef: Ref


class PullRequest(BaseModel):
    title: str
    description: str
    fromRef: Ref
    toRef: Ref
    state: PRState
    id: int
    version: int


class Page(BaseModel):
    size: int
    limit: int
    isLastPage: bool
    values: List[Any]
    start: int
    nextPageStart: Optional[int]
