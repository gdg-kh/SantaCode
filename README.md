# SantaCode 🎅💻

歡迎來到工程師的交換禮物活動！
Welcome to the Programmer's Secret Santa!

## 📜 規則 (Rules)

1.  **目標 (Goal)**: 寫一個程式，執行後會在 Standard Output (stdout) 印出一棵聖誕樹。
    Write a program that prints a Christmas tree to stdout.
2.  **語言 (Languages)**: 支援 Python, JavaScript (Node.js), Go, Ruby, Rust, C, C++, C#, Java, Kotlin, Swift (只要能用標準 Docker Image 跑起來)。
3.  **限制 (Constraints)**:
    - **NO Internet**: 執行環境沒有網路。
    - **Standard Library Only**: 禁止安裝第三方套件 (`npm install`, `pip install` ... etc are NOT allowed)。
    - **Time Limit**: 5 秒內必須執行完畢。
4.  **如何參加 (How to Join)**:
    - <a href="https://github.com/gdg-kh/SantaCode/fork" style="color: white;">將本專案 Fork 到你的 GitHub。</a>
    - 在 `submissions/` 下建立一個你的 **GitHub ID** 資料夾 (e.g., `submissions/torvalds/`).
    - 放入你的程式碼，檔案命名為 `tree.使用的程式語言` (e.g., `tree.py`, `tree.js`, `tree.go` ... etc).
    - 發送 [Pull Request](https://github.com/gdg-kh/SantaCode/pulls) 到本 Repo。


## 🧪 本地測試 (Local Test)

如果你有裝 Docker，可以用以下指令模擬 CI 環境：

| Language | Docker Image |
|----------|:-------------:|
| Python | `python:3.10-slim` |
| Node JS | `node:18-alpine` |
| Golang | `golang:1.20-alpine` |
| Ruby | `ruby:3.2-alpine` |
| Rust | `rust:slim` |
| C | `gcc:12` |
| C++ | `gcc:12` |
| C# | `mono:6.12` |
| Java | `openjdk:17-jdk-slim` |
| Kotlin | `zenika/kotlin:1.8` |
| Swift | `swift:5.8-slim` |

你需要調整的

1. `YOUR_ID` 換成你的 GitHub ID
2. 選擇使用的語言對應的 Docker Image
3. `python tree.py` 換成你的執行的語言和程式碼檔名

Python 範例指令如下：

```bash
docker run --rm --network none --memory 512m -v $(pwd)/submissions/example-santa:/app -w /app python:3.10-slim python tree.py
```

## 🎁 交換 (Exchange)

活動截止後，Repo 管理員會按下「交換按鈕」。系統會自動亂數配對，並在 Issues 中標記你，讓你收到別人的程式碼執行結果！
