from dataclasses import dataclass, field
from functools import lru_cache
from http import HTTPStatus
from typing import List, Dict

from fastapi import Depends, APIRouter, FastAPI
from starlette.testclient import TestClient

from .types import PullRequest, NewPullRequest, PRState, Page


router = APIRouter(
    prefix="/rest/api/1.0/projects/{project_key}/repos/{repository_slug}"
)


@dataclass
class RepoState:
    prs: List[PullRequest] = field(default_factory=list)
    counter: int = 0


@dataclass
class ProjectState:
    repos: Dict[str, RepoState] = field(default_factory=dict)


@dataclass
class State:
    projects: Dict[str, ProjectState] = field(default_factory=dict)


@lru_cache
def get_state() -> State:
    return State()


def get_project(project_key: str, state: State = Depends(get_state)) -> ProjectState:
    return state.projects.setdefault(project_key, ProjectState())


def get_repo(
    repository_slug: str, project: ProjectState = Depends(get_project)
) -> RepoState:
    return project.repos.setdefault(repository_slug, RepoState())


@router.post(
    "/pull-requests",
    status_code=HTTPStatus.CREATED,
)
def create_pull_request(pr: NewPullRequest, repo: RepoState = Depends(get_repo)):
    repo.prs.append(PullRequest(state="OPEN", id=repo.counter, version=0, **pr.dict()))
    repo.counter = repo.counter + 1


@router.get("/pull-requests/{pr_id}")
def get_pull_request(pr_id: int, repo: RepoState = Depends(get_repo)) -> PullRequest:
    matching = [pr for pr in repo.prs if pr.id == pr_id]
    return matching[0]


@router.post("/pull-requests/{pr_id}/decline")
def decline_pull_request(pr_id: int, version: int, repo: RepoState = Depends(get_repo)):
    matching = [pr for pr in repo.prs if pr.id == pr_id]
    assert matching[0].version == version
    matching[0].state = "DECLINED"


@router.post("/pull-requests/{pr_id}/merge")
def merge_pull_request(pr_id: int, version: int, repo: RepoState = Depends(get_repo)):
    matching = [pr for pr in repo.prs if pr.id == pr_id]
    assert matching[0].version == version
    matching[0].state = "MERGED"


@router.get("/pull-requests")
def get_pull_requests(
    repo: RepoState = Depends(get_repo),
    limit: int = 50,
    start: int = 0,
    state: PRState = "ALL",
):
    prs = [pr for pr in repo.prs if state == "ALL" or pr.state == state]
    is_last_page = start + limit >= len(prs)
    return Page(
        size=min(len(prs) - start, limit),
        limit=limit,
        start=start,
        isLastPage=is_last_page,
        nextPageStart=None if is_last_page else start + limit,
        values=prs[start:limit],
    )


@dataclass
class BitbucketMock:
    _state: State = field(init=False, default_factory=State)
    _app: FastAPI = field(init=False, default_factory=FastAPI)

    def __post_init__(self):
        self._app.dependency_overrides[get_state] = lambda: self._state
        self._app.include_router(router)

    def get_test_client(self) -> TestClient:
        return TestClient(self._app)
