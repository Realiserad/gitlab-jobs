#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
from datetime import timedelta, datetime

GITLAB_BASE_URL = os.environ['BASE_URL']
GITLAB_API_TOKEN = os.environ['GITLAB_API_TOKEN']
ROTTEN_LABEL = os.environ['ROTTEN_LABEL']
CLOSE_AFTER = int(os.environ['CLOSE_AFTER'])
PROJECTS = os.environ['PROJECTS']


def get_rotten_mrs(project_id, updated_before):
    page = 1
    while True:
        url = f"{GITLAB_BASE_URL}/api/v4/projects/{project_id}/merge_requests"
        headers = {"PRIVATE-TOKEN": GITLAB_API_TOKEN}
        params = {
            "state": "opened",
            "view": "simple",
            "page": page,
            "labels": ROTTEN_LABEL,
            "updated_before": updated_before}
        response = requests.get(
            url,
            headers=headers,
            params=params)
        if response.status_code != 200:
            raise Exception("Failed to get open merge requests: " +
                            response.text)
        if len(response.json()) == 0:
            return
        for mr in response.json():
            yield mr["iid"]
        page += 1


def close_rotten_mrs(project):
    print(f"🤖 Looking for rotten merge requests to close in '{project}'.")
    print(f"A merge request is closed {CLOSE_AFTER} days after being marked "
          "as rotten.")

    response = requests.get(
        f"{GITLAB_BASE_URL}/api/v4/projects/{project.replace('/', '%2F')}",
        headers={"PRIVATE-TOKEN": GITLAB_API_TOKEN})
    if response.status_code != 200:
        raise Exception(f"Failed to get project ID: {response.text}")

    project_id = response.json()["id"]
    updated_before = (datetime.now() -
                      timedelta(days=CLOSE_AFTER)).isoformat() + "Z"
    for rotten_mr in get_rotten_mrs(project_id, updated_before):
        print(f"🌒 Merge request #{rotten_mr} is being closed.")
        response = requests.put(
            f"{GITLAB_BASE_URL}/api/v4/projects/{project_id}/merge_requests/"
            f"{rotten_mr}",
            headers={"PRIVATE-TOKEN": GITLAB_API_TOKEN},
            params={"state_event": "close"})
        if response.status_code < 200 or response.status_code > 299:
            raise Exception(f"Failed to close merge request: {response.text}")


for project in PROJECTS.replace(",", " ").split():
    close_rotten_mrs(project)
