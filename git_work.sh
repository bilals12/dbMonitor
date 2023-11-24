#!/bin/bash

# check for required args
if [ $# -lt 1 ]; then
    echo "usage: $0 <branch_pattern"
    exit 1
fi

branch_pattern=$1

# fetch and compare branches
git fetch --all

# find highest numbered remote and local branches matching the pattern (latest version)
remote_branch=$(git branch -r | grep "$branch_pattern" | sort -r | head -n 1)
local_branch=$(git branch | grep "$branch_pattern" | sort -r | head -n 1 | tr "*" " ")

# checkout new branch if needed
if [[ $remote_branch != *"$local_branch"* ]]; then
    echo "switching to branch: $remote_branch"
    git checkout -b "$remote_branch" --track "origin/$remote_branch"
else
    git pull
fi