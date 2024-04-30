#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
from datetime import timedelta, datetime

GITLAB_API_TOKEN = os.environ['GITLAB_API_TOKEN']
GITLAB_BASE_URL = os.environ['GITLAB_BASE_URL']
ROTTEN_AFTER = int(os.environ['ROTTEN_AFTER'])
ROTTEN_LABEL = os.environ['ROTTEN_LABEL']
PROJECTS = os.environ['PROJECTS']


def get_open_mrs(project_id, updated_before):
    page = 1
    while True:
        url = f"{GITLAB_BASE_URL}/api/v4/projects/{project_id}/merge_requests"
        headers = {"PRIVATE-TOKEN": GITLAB_API_TOKEN}
        params = {
            "state": "opened",
            "updated_before": updated_before,
            "page": page
        }
        response = requests.get(
            url,
            headers=headers,
            params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to get open merge requests: "
                            f"{response.text}")
        if len(response.json()) == 0:
            return
        new_rotten_mrs = [mr["iid"] for mr in response.json()
                          if ROTTEN_LABEL not in mr["labels"]]
        for mr in new_rotten_mrs:
            yield mr
        page += 1


def mark_rotten_mrs(project):
    print(f"🤖 Now looking for merge requests to be marked as rotten "
          f"in '{project}'.")
    print(f"A merge request is considered rotten after being inactive "
          f"for {ROTTEN_AFTER} days.")
    updated_before = (datetime.now() -
                      timedelta(days=ROTTEN_AFTER)).isoformat() + "Z"
    response = requests.get(
        url=f"{GITLAB_BASE_URL}/api/v4/projects/{project.replace('/', '%2F')}",
        headers={"PRIVATE-TOKEN": GITLAB_API_TOKEN})
    if response.status_code != 200:
        raise Exception(f"Failed to get project ID: {response.text}")
    project_id = response.json()["id"]
    for open_mr in get_open_mrs(project_id, updated_before):
        print(f"🌒 Merge request #{open_mr} is rotten.")
        response = requests.post(
            url=f"{GITLAB_BASE_URL}/api/v4/projects/{project_id}/"
            f"merge_requests/{open_mr}/notes",
            headers={"PRIVATE-TOKEN": GITLAB_API_TOKEN},
            params={"body": f"/label ~{ROTTEN_LABEL}"})
        if response.status_code < 200 or response.status_code > 299:
            raise Exception(f"Failed to add label to merge request: "
                            f"{response.text}")
        comment = ("🌒 The merge request has been inactive for "
                   f"{ROTTEN_AFTER} days and will be marked as rotten. "
                   "To prevent this merge request from being automatically "
                   f"closed, comment with `/unlabel ~{ROTTEN_LABEL}`. ")
        response = requests.post(
            url=f"{GITLAB_BASE_URL}/api/v4/projects/{project_id}/"
            f"merge_requests/{open_mr}/notes",
            headers={"PRIVATE-TOKEN": GITLAB_API_TOKEN},
            params={"body": comment})
        if response.status_code < 200 or response.status_code > 299:
            raise Exception(f"Failed to comment on merge request: "
                            f"{response.text}")


for project in PROJECTS.replace(",", " ").split():
    mark_rotten_mrs(project)
