# About

Container with various housekeeping scripts for GitLab which can be deployed
as a Kubernetes `Job` or `CronJob`.

## Deploy with Helm

1.
    Add a bot user in GitLab and [create a personal access token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#create-a-personal-access-token).

2.
    Deploy a secret for the bot containing using `kubectl`:

    ```shell
    kubectl create secret generic gitlab-api \
        --from-literal=username=<USERNAME> \
        --from-literal=email=<EMAIL> \
        --from-literal=token=<TOKEN>
    ```

3.
    Customise [the `values.yaml`](https://github.com/Realiserad/gitlab-jobs/blob/main/chart/values.yaml)
    according to your needs. You probably want to adjust `gitlab.url` and `projects`.

4.
    Install the Helm chart:

    ```shell
    helm install oci://ghcr.io/realiserad/charts/gitlab-jobs --version 0.3.0 --values values.yaml
    ```

5.
    Sit back and relax while Kubernetes takes care of automating your GitLab instance. 🍷

## Implemented jobs

All jobs can be found in the `jobs` folder.

All jobs must run with the following environment variables set:

- `GITLAB_BASE_URL`: The base URL of the GitLab instance, e.g. `https://gitlab.company.com`.
- `$GITLAB_API_TOKEN`: The API token used to authenticate to GitLab.

### `mark-rotten`

Mark merge requests that have been inactive for the specified amount of time
as rotten.

#### Parameters

- `$ROTTEN_AFTER`: The number of days that a merge request must have been
inactive before it is marked as rotten.
- `PROJECTS`: A comma-separated list of projects to search for rotten merge
requests, e.g. `owner/repo1,owner/repo2`.

### `close-rotten`

Close merge requests marked as rotten.

#### Parameters

- `PROJECTS`: A comma-separated list of projects where rotten merge requests
should be closed, e.g. `owner/repo1,owner/repo2`.
- `CLOSE_AFTER`: The number of days that a merge request must have been marked
as rotten before it is closed.

### `create-foreign-aliases`

Creates an `OWNERS_ALIASES` file compatible with
[Jenkins X foreign aliases](https://jenkins-x.io/blog/2023/02/09/foreign-aliases/)
from the group permissions on your GitLab instance.

#### Parameters

- `PROJECT`: The name of the project where the `OWNERS_ALIASES` file should be
  created, e.g. `owner/repo`.
- `COMMITTER_NAME`: The name of your GitLab bot. Used for commits.
- `COMMITTER_EMAIL`: The email of your GitLab bot. Used for commits.
