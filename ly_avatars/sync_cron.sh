#!/bin/bash
# LY化身系统定时同步脚本
cd /workspace/projects/workspace
python3 ly_avatars/avatar_manager.py sync >> /workspace/projects/workspace/ly_avatars/sync.log 2>&1
