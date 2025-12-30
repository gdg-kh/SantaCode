import os
import random
import csv
import glob
import shutil
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
    supported_exts = ['.py', '.js', '.go', '.rb', '.sh', '.java', '.kt', '.swift', '.c', '.cpp', '.cs', '.rs']
    
    for user_dir in SUBMISSIONS_DIR.iterdir():
        if user_dir.is_dir() and not user_dir.name.startswith('.') and user_dir.name != 'example-santa':
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
    
    # 建立禮物存放根目錄
    gifts_root = BASE_DIR / "received_gifts"
    if gifts_root.exists():
        shutil.rmtree(gifts_root)
    gifts_root.mkdir(exist_ok=True)

    for sender, receiver in zip(participants, receivers):
        print(f"Process: {sender['id']} -> {receiver['id']}")
        
        # 執行 Sender 的程式碼 (這是送給 Receiver 的禮物)
        success, output = run_in_docker(str(sender['file']))
        
        status = "Success" if success else "Failed"
        gift_content = output if success else f"Error: {output}"
        
        # 簡單的保底機制：如果失敗，換成官方文字樹
        if not success:
            gift_content = f"[System] The code from {sender['id']} broke. Here is a backup tree:\n   *\n  /|\\\\\n /_|_\\\\\n   |"

        # --- 新增功能：儲存實體禮物檔案 ---
        receiver_gift_dir = gifts_root / receiver['id']
        receiver_gift_dir.mkdir(parents=True, exist_ok=True)

        # 1. 複製原始碼
        sender_file_path = sender['file']
        # 檔名格式: from_{SenderID}_{OriginalName}
        dest_filename = f"from_{sender['id']}_{sender_file_path.name}"
        shutil.copy2(sender_file_path, receiver_gift_dir / dest_filename)

        # 2. 儲存執行結果為 Markdown
        md_filename = f"gift_from_{sender['id']}.md"
        with open(receiver_gift_dir / md_filename, "w", encoding="utf-8") as md_file:
            md_content = f"""# 🎁 Gift from {sender['id']}

## Status: {status}

## 🎄 The Tree (Output)
```
{gift_content}
```

## 📜 Source Code
The original source code (`{sender_file_path.name}`) has been included in this folder as `{dest_filename}`.
"""
            md_file.write(md_content)
        # -----------------------------------

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
            
    # --- 新增功能：產生總結 Issue 內容 ---
    issue_file = "final_issue_body.md"
    with open(issue_file, "w", encoding="utf-8") as f:
        f.write("# 🎅 2025 Secret Santa 禮物派發完成！\n\n")
        f.write("大家的禮物都已經生成完畢，請在下方表格找到你的名字，點擊連結領取禮物！\n\n")
        f.write("| Receiver (你) | Sender (送禮者) | 狀態 | 你的禮物連結 |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        for data in results:
            # 使用 @Tag 提醒參與者
            receiver_tag = f"@{data['Receiver']}"
            sender_name = data['Sender']
            status_emoji = "✅" if data['Status'] == "Success" else "⚠️ (Backup)"
            gift_link = f"[查看我的禮物](./received_gifts/{data['Receiver']})"
            f.write(f"| {receiver_tag} | {sender_name} | {status_emoji} | {gift_link} |\n")
        
        f.write("\n\n---\n*本活動由 SantaCode 自動化系統執行。祝大家新年快樂！* 🎄")

    print(f"✅ Exchange complete! Report saved to {REPORT_FILE}")
    print(f"📢 Summary Issue body generated: {issue_file}")

if __name__ == "__main__":
    main()
