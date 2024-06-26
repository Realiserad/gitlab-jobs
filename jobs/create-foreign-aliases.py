#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import yaml
import os

GITLAB_BASE_URL = os.environ['GITLAB_BASE_URL']
GITLAB_API_TOKEN = os.environ['GITLAB_API_TOKEN']
MAINTAINER_ACCESS_LEVEL = 40
REPORTER_ACCESS_LEVEL = 20


def get_groups():
    return json.loads(requests.get(
        url=f"{GITLAB_BASE_URL}/api/v4/groups",
        headers={"PRIVATE-TOKEN": GITLAB_API_TOKEN}).text)


def get_members(group_id, min_access_level):
    members = json.loads(requests.get(
        url=f"{GITLAB_BASE_URL}/api/v4/groups/{group_id}/members",
        headers={"PRIVATE-TOKEN": GITLAB_API_TOKEN}).text)
    return [member["username"] for member in members
            if member['access_level'] >= min_access_level]


def normalize(name):
    return name.lower().replace(" ", "-")


approvers = [(normalize(group['name']) + "-approvers",
              get_members(
    group_id=group["id"],
    min_access_level=MAINTAINER_ACCESS_LEVEL)
) for group in get_groups()
]
reviewers = [(normalize(group['name']) + "-reviewers",
              get_members(
                  group_id=group["id"],
                  min_access_level=REPORTER_ACCESS_LEVEL))
             for group in get_groups()]

with open('OWNERS_ALIASES', 'w') as f:
    f.write('# This file is autogenerated. Do not edit!\n')
    f.write(yaml.dump({
        "aliases": {k: v for (k, v) in approvers + reviewers}
    }))
