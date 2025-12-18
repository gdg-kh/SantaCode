#!/usr/bin/env python3
"""
本地測試腳本 - 在提交前驗證所有 Docker 映像檔和功能
"""
import subprocess
import sys
import os
from pathlib import Path
from core.runner import LANGUAGE_CONFIG

# Docker 可能的路徑
DOCKER_PATHS = [
    '/usr/local/bin/docker',
    '/opt/homebrew/bin/docker',
    'docker'  # fallback to PATH
]

def find_docker():
    """尋找 Docker 執行檔"""
    for path in DOCKER_PATHS:
        try:
            result = subprocess.run([path, '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                return path
        except:
            continue
    return None

DOCKER_CMD = find_docker()

def check_docker():
    """檢查 Docker 是否可用"""
    print("🔍 檢查 Docker 環境...")
    if not DOCKER_CMD:
        print("❌ 找不到 Docker 指令，請先安裝 Docker")
        return False

    try:
        result = subprocess.run([DOCKER_CMD, '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker 已安裝: {result.stdout.strip()}")
            return True
        else:
            print("❌ Docker 未正確安裝")
            return False
    except Exception as e:
        print(f"❌ Docker 檢查失敗: {str(e)}")
        return False

def pull_docker_images():
    """預先拉取所有需要的 Docker 映像檔"""
    print("\n📥 拉取所有需要的 Docker 映像檔...")
    images = set(config['image'] for config in LANGUAGE_CONFIG.values())

    failed_images = []
    for image in sorted(images):
        print(f"  拉取 {image}...", end=" ")
        try:
            result = subprocess.run(
                [DOCKER_CMD, 'pull', image],
                capture_output=True,
                text=True,
                timeout=300  # 5分鐘超時
            )
            if result.returncode == 0:
                print("✅")
            else:
                print(f"❌\n    錯誤: {result.stderr.strip()}")
                failed_images.append(image)
        except subprocess.TimeoutExpired:
            print("❌ (超時)")
            failed_images.append(image)
        except Exception as e:
            print(f"❌ ({str(e)})")
            failed_images.append(image)

    if failed_images:
        print(f"\n❌ 以下映像檔拉取失敗:")
        for img in failed_images:
            print(f"  - {img}")
        return False
    else:
        print("\n✅ 所有映像檔拉取成功")
        return True

def test_runner():
    """測試 runner.py 是否能正常執行範例檔案"""
    print("\n🧪 測試 runner.py...")

    # 尋找範例檔案
    submissions_dir = Path(__file__).parent / "submissions"
    if not submissions_dir.exists():
        print("⚠️  找不到 submissions 目錄，跳過 runner 測試")
        return True

    # 找一個測試檔案
    test_file = submissions_dir / "example-santa" / "tree.sh"
    if not test_file.exists():
        print("⚠️  找不到測試檔案，跳過 runner 測試")
        return True

    print(f"  測試檔案: {test_file}")
    try:
        result = subprocess.run(
            [sys.executable, 'core/runner.py', str(test_file)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("✅ Runner 執行成功")
            print(f"  輸出: {result.stdout[:100]}..." if len(result.stdout) > 100 else f"  輸出: {result.stdout}")
            return True
        else:
            print(f"❌ Runner 執行失敗")
            print(f"  錯誤: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Runner 測試出錯: {str(e)}")
        return False

def test_exchange():
    """測試 exchange.py 是否能正常執行"""
    print("\n🎅 測試 exchange.py (完整流程)...")

    try:
        result = subprocess.run(
            [sys.executable, 'core/exchange.py'],
            capture_output=True,
            text=True,
            timeout=120  # 2分鐘超時
        )
        print(result.stdout)

        if result.returncode == 0:
            print("\n✅ Exchange 執行成功")

            # 檢查報表是否生成
            report_file = Path("match_report.csv")
            if report_file.exists():
                print(f"✅ 報表已生成: {report_file}")
                return True
            else:
                print("⚠️  報表未生成")
                return False
        else:
            print(f"\n❌ Exchange 執行失敗")
            print(f"錯誤: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Exchange 執行超時")
        return False
    except Exception as e:
        print(f"❌ Exchange 測試出錯: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🎄 SantaCode 本地測試工具")
    print("=" * 60)

    # 1. 檢查 Docker
    if not check_docker():
        print("\n❌ 測試失敗: Docker 環境未就緒")
        sys.exit(1)

    # 2. 拉取映像檔
    if not pull_docker_images():
        print("\n❌ 測試失敗: 無法拉取所有 Docker 映像檔")
        print("\n💡 建議:")
        print("  1. 檢查網路連線")
        print("  2. 檢查 Docker Hub 是否可訪問")
        print("  3. 驗證映像檔名稱和版本是否正確")
        sys.exit(1)

    # 3. 測試 runner
    if not test_runner():
        print("\n❌ 測試失敗: Runner 無法正常執行")
        sys.exit(1)

    # 4. 測試 exchange
    if not test_exchange():
        print("\n❌ 測試失敗: Exchange 無法正常執行")
        sys.exit(1)

    # 所有測試通過
    print("\n" + "=" * 60)
    print("✅ 所有測試通過！可以安全地提交程式碼")
    print("=" * 60)
    print("\n下一步:")
    print("  1. git add .")
    print("  2. git commit -m 'fix: 更新 Kotlin Docker 映像檔版本'")
    print("  3. git push")
    sys.exit(0)

if __name__ == "__main__":
    main()
