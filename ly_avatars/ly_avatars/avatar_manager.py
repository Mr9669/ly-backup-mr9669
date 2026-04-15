"""
LY化身管理器 v2.3
管理化身系统，执行数据同步
"""

import os
import json
import subprocess
from datetime import datetime

AVATARS_FILE = "/workspace/projects/workspace/ly_avatars/avatars.json"
BACKUP_DIR = "/workspace/projects/workspace"
GITHUB_USER = "Mr9669"
GITHUB_REPO = "ly-backup-mr9669"

def get_github_token():
    """从环境变量获取GitHub Token"""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        config_file = "/workspace/projects/workspace/ly_avatars/.env"
        if os.path.exists(config_file):
            with open(config_file) as f:
                for line in f:
                    if line.startswith("GITHUB_TOKEN="):
                        return line.split("=", 1)[1].strip()
        print("❌ 未设置GITHUB_TOKEN")
        return None
    return token

def run_cmd(cmd, cwd=None, check=True):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"命令失败: {' '.join(cmd)}")
        print(result.stdout)
        print(result.stderr)
    return result

class AvatarManager:
    def __init__(self):
        self.avatars = self.load_avatars()
    
    def load_avatars(self):
        if os.path.exists(AVATARS_FILE):
            with open(AVATARS_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    def list_avatars(self):
        print("\n" + "="*50)
        print("LY化身系统 - 节点列表")
        print("="*50)
        for node_id, info in self.avatars.items():
            status = "✅" if info.get("status") == "active" else "⏳"
            print(f"{status} {node_id}")
            print(f"   类型: {info.get('type', 'unknown')}")
            print(f"   平台: {info.get('platform', {}).get('name', 'unknown')}")
            print(f"   状态: {info.get('status', 'unknown')}")
            print()
    
    def sync_to_github(self):
        """同步数据到GitHub"""
        token = get_github_token()
        if not token:
            return False
            
        repo_url = f"https://{GITHUB_USER}:{token}@github.com/{GITHUB_USER}/{GITHUB_REPO}.git"
        print("\n开始同步到GitHub...")
        
        temp_dir = f"/tmp/ly-sync-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            run_cmd(["git", "clone", "--depth", "1", repo_url, temp_dir])
            run_cmd(["git", "config", "user.email", "19821319669@163.com"], cwd=temp_dir)
            run_cmd(["git", "config", "user.name", "LY Avatar"], cwd=temp_dir)
            
            # 复制文件
            for d in ["memory", "ly_avatars"]:
                src = os.path.join(BACKUP_DIR, d)
                dst = os.path.join(temp_dir, d)
                if os.path.exists(src):
                    run_cmd(["cp", "-r", src, dst])
            
            for f in ["MEMORY.md", "AGENTS.md", "SOUL.md", "USER.md", "IDENTITY.md", "HEARTBEAT.md"]:
                src = os.path.join(BACKUP_DIR, f)
                dst = os.path.join(temp_dir, f)
                if os.path.exists(src):
                    run_cmd(["cp", src, dst])
            
            run_cmd(["git", "add", "."], cwd=temp_dir)
            
            result = run_cmd(["git", "status", "--porcelain"], cwd=temp_dir, check=False)
            if not result.stdout.strip():
                print("没有变化")
                return True
            
            commit_msg = f"LY备份 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            run_cmd(["git", "commit", "-m", commit_msg], cwd=temp_dir)
            result = run_cmd(["git", "push", "-u", "origin", "main"], cwd=temp_dir, check=False)
            
            if result.returncode == 0:
                print(f"✅ 同步成功!")
                return True
            else:
                print(f"❌ 推送失败: {result.stderr}")
                return False
            
        except Exception as e:
            print(f"❌ 同步失败: {e}")
            return False
        finally:
            subprocess.run(["rm", "-rf", temp_dir], capture_output=True)

def main():
    manager = AvatarManager()
    
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "list":
            manager.list_avatars()
        elif cmd == "sync":
            manager.sync_to_github()
        else:
            print("命令: list|sync")
    else:
        manager.list_avatars()

if __name__ == "__main__":
    main()
