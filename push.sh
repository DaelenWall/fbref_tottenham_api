#!/bin/bash

# Check if commit message was provided
if [ -z "$1" ]; then
  echo "❌ Please provide a commit message!"
  echo "Usage: ./push.sh \"Your commit message\""
  exit 1
fi

# Add all changes
git add .

# Commit with provided message
git commit -m "$1"

# Push to main branch
git push
