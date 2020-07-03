#!/bin/sh

if [ "`git status -s`" ]
then
    echo "The working directory is dirty. Please commit any pending changes."
    exit 1;
fi

echo "Deleting old _build"
rm -rf _build
mkdir _build
git worktree prune
rm -rf .git/worktrees/_build/

echo "Checking out gh-pages branch into _build"
git worktree add -B gh-pages _build upstream/gh-pages

echo "Removing existing files"
rm -rf _build/*

echo "Generating site"
make build

echo "Updating gh-pages branch"
cd _build && git add --all && git commit -m "Publishing to gh-pages (publish.sh)"

#echo "Pushing to github"
#git push --all