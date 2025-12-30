import subprocess
import os
from pathlib import Path

def post_summary_issue():
    issue_file = Path("final_issue_body.md")
    if not issue_file.exists():
        print("Error: final_issue_body.md not found. Run exchange.py first.")
        return

    print("🚀 Posting summary Issue to GitHub...")
    
    title = "🎁 2025 Secret Santa 禮物派發完成！"
    
    try:
        # 使用 gh issue create 指令
        # --title 設定標題
        # --body-file 直接讀取 md 檔案內容作為內文
        result = subprocess.run([
            "gh", "issue", "create",
            "--title", title,
            "--body-file", str(issue_file)
        ], capture_output=True, text=True, check=True)
        
        print(f"✅ Issue created successfully!")
        print(f"URL: {result.stdout.strip()}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create issue: {e.stderr}")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    post_summary_issue()
