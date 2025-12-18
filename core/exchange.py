import os
import random
import csv
import glob
from pathlib import Path
from runner import run_in_docker

# 設定路徑
BASE_DIR = Path(__file__).parent.parent
SUBMISSIONS_DIR = BASE_DIR / "submissions"
REPORT_FILE = "match_report.csv"

def get_participants():
    # 尋找 submissions/ 下的每個資料夾，假設資料夾名稱就是 User ID
    # 並且裡面必須要有支援的程式碼檔案
    participants = []
    supported_exts = ['.py', '.js', '.go', '.rb', '.sh']
    
    for user_dir in SUBMISSIONS_DIR.iterdir():
        if user_dir.is_dir() and not user_dir.name.startswith('.'):
            # 找找看有沒有程式碼
            code_files = []
            for ext in supported_exts:
                code_files.extend(list(user_dir.glob(f"*{ext}")))
            
            if code_files:
                # 取第一個找到的程式碼當作參賽作品
                participants.append({
                    "id": user_dir.name,
                    "file": code_files[0]
                })
    return participants

def derangement_shuffle(lst):
    """
    產生錯位排列 (Derangement)：確保沒有人配對到自己
    """
    if len(lst) < 2:
        return None # 無法交換
        
    original = lst[:]
    shuffled = lst[:]
    
    while True:
        random.shuffle(shuffled)
        # 檢查是否有任何位置的元素相同
        if all(x != y for x, y in zip(original, shuffled)):
            return shuffled

def main():
    print("🎅 Starting Secret Santa Exchange... 🎄")
    
    participants = get_participants()
    count = len(participants)
    print(f"Found {count} participants.")
    
    if count < 2:
        print("Not enough participants to exchange! (Need at least 2)")
        return

    # 進行配對
    receivers = derangement_shuffle(participants)
    
    results = []
    
    print("🎁 Exchanging gifts...")
    for sender, receiver in zip(participants, receivers):
        print(f"Process: {sender['id']} -> {receiver['id']}")
        
        # 執行 Sender 的程式碼 (這是送給 Receiver 的禮物)
        success, output = run_in_docker(str(sender['file']))
        
        status = "Success" if success else "Failed"
        gift_content = output if success else f"Error: {output}"
        
        # 簡單的保底機制：如果失敗，換成官方文字樹
        if not success:
             gift_content = f"[System] The code from {sender['id']} broke. Here is a backup tree:\n   *\n  /|\\\n /_|_\\\n   |"

        results.append({
            "Sender": sender['id'],
            "Receiver": receiver['id'],
            "Status": status,
            "GiftPreview": gift_content[:100].replace('\n', ' ') + "..." # 預覽前100字
        })

    # 輸出 CSV 報表
    with open(REPORT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Sender', 'Receiver', 'Status', 'GiftPreview']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for data in results:
            writer.writerow(data)
            
    print(f"✅ Exchange complete! Report saved to {REPORT_FILE}")

if __name__ == "__main__":
    main()
