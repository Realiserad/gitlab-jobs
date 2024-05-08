#!/bin/sh

set -e

echo "👷 Collecting foreign aliases from GitLab..."
/jobs/create-foreign-aliases.py

echo "🐑 Cloning $PROJECT..."
GIT_CLONE_URI="https://$COMMITTER_NAME:$GITLAB_API_TOKEN@$(echo "$GITLAB_BASE_URL" | sed 's|https://||g')/$PROJECT.git"
git clone --filter=blob:none --branch main --single-branch "$GIT_CLONE_URI" source
cp OWNERS_ALIASES source
cd source

echo "🧰 Creating git config for $COMMITTER_NAME..."
git config --global user.email "$COMMITTER_EMAIL"
git config --global user.name "$COMMITTER_NAME"

echo "🤖 Committing OWNERS_ALIASES..."
git add OWNERS_ALIASES
git commit -m "chore: update owners aliases" || true

echo "🚀 Pushing changes (if any)..."
git push