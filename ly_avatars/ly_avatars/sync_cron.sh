#!/bin/bash
# 从环境变量或本地文件读取Token
TOKEN=$(cat /workspace/ly_github_token.bak 2>/dev/null || echo "$GITHUB_TOKEN")
export GITHUB_TOKEN="$TOKEN"
cd /workspace/projects/workspace
python3 ly_avatars/avatar_manager.py sync >> /workspace/projects/workspace/ly_avatars/sync.log 2>&1
