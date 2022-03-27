# BitbucketMock
lightweight mock for bitbucket's REST API

## When should I use this?
**This project does not strive to implement each endpoint with 100% accuracy**, even if the endpoint exists, it might not be fully implemented.

Therefore, it is not recommanded for use in CI pipelines, but instead is meant to be used when developing your application locally.

Since bitbucket is eventually-consistent and might delay actions, this will reduce a lot of time from the tests.
