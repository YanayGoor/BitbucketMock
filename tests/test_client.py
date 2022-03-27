def test_get_prs(client):
    response = client.get("/rest/api/1.0/projects/PRJ/repos/myrepo/pull-requests")
    assert response.ok, response.content
    assert response.json() == {
        "isLastPage": True,
        "limit": 50,
        "nextPageStart": None,
        "size": 0,
        "start": 0,
        "values": [],
    }


def test_create_pr(client):
    response = client.post(
        "/rest/api/1.0/projects/PRJ/repos/myrepo/pull-requests",
        json={
            "title": "Open PR",
            "description": "bla bla",
            "fromRef": {
                "id": "refs/heads/feature-ABC-123",
                "repository": {
                    "slug": "myrepo",
                    "name": None,
                    "project": {"key": "PRJ"},
                },
            },
            "toRef": {
                "id": "refs/heads/master",
                "repository": {
                    "slug": "myrepo",
                    "name": None,
                    "project": {"key": "PRJ"},
                },
            },
        },
    )
    assert response.ok, response.content

    response = client.get("/rest/api/1.0/projects/PRJ/repos/myrepo/pull-requests")
    assert response.ok, response.content
    assert response.json() == {
        "isLastPage": True,
        "limit": 50,
        "nextPageStart": None,
        "size": 1,
        "start": 0,
        "values": [
            {
                "description": "bla bla",
                "fromRef": {
                    "id": "refs/heads/feature-ABC-123",
                    "repository": {
                        "name": None,
                        "project": {"key": "PRJ"},
                        "slug": "myrepo",
                    },
                },
                "id": 0,
                "state": "OPEN",
                "title": "Open PR",
                "toRef": {
                    "id": "refs/heads/master",
                    "repository": {
                        "name": None,
                        "project": {"key": "PRJ"},
                        "slug": "myrepo",
                    },
                },
                "version": 0,
            }
        ],
    }
