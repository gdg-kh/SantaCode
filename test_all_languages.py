#!/usr/bin/env python3
"""
測試所有語言的 Docker 映像檔是否能正常工作
"""
import subprocess
import sys
from pathlib import Path
from core.runner import LANGUAGE_CONFIG

def test_all_languages():
    """測試所有語言配置"""
    print("=" * 60)
    print("🧪 測試所有語言的 Docker 映像檔")
    print("=" * 60)

    example_dir = Path("submissions/example-santa")
    if not example_dir.exists():
        print("❌ 找不到 example-santa 目錄")
        return False

    # 收集所有語言的測試結果
    results = {}
    failed_tests = []

    # 對每種語言執行測試
    for ext, config in LANGUAGE_CONFIG.items():
        # 尋找對應的測試檔案
        test_files = list(example_dir.glob(f"*{ext}"))

        if not test_files:
            print(f"\n⚠️  {ext}: 找不到測試檔案")
            continue

        test_file = test_files[0]
        print(f"\n{'=' * 60}")
        print(f"🧪 測試語言: {ext}")
        print(f"   映像檔: {config['image']}")
        print(f"   測試檔: {test_file.name}")
        print(f"{'=' * 60}")

        try:
            result = subprocess.run(
                [sys.executable, 'core/runner.py', str(test_file)],
                capture_output=True,
                text=True,
                timeout=120  # Allow enough time for Go compilation
            )

            if result.returncode == 0:
                print(f"✅ {ext} - Docker 映像檔工作正常")
                results[ext] = "✅ PASS"

                # 驗證輸出
                validator_result = subprocess.run(
                    [sys.executable, 'challenges/2025-tree/validator.py'],
                    input=result.stdout,
                    capture_output=True,
                    text=True
                )

                if validator_result.returncode == 0:
                    print(f"   ✅ 輸出驗證通過")
                else:
                    print(f"   ⚠️  輸出驗證失敗（但 Docker 映像檔能運行）")
            else:
                print(f"❌ {ext} - 執行失敗")
                print(f"   錯誤: {result.stderr}")
                results[ext] = "❌ FAIL"
                failed_tests.append({
                    'ext': ext,
                    'image': config['image'],
                    'error': result.stderr
                })

        except subprocess.TimeoutExpired:
            print(f"❌ {ext} - 執行超時")
            results[ext] = "❌ TIMEOUT"
            failed_tests.append({
                'ext': ext,
                'image': config['image'],
                'error': 'Timeout after 60 seconds'
            })
        except Exception as e:
            print(f"❌ {ext} - 執行出錯: {str(e)}")
            results[ext] = "❌ ERROR"
            failed_tests.append({
                'ext': ext,
                'image': config['image'],
                'error': str(e)
            })

    # 輸出總結
    print("\n" + "=" * 60)
    print("📊 測試總結")
    print("=" * 60)

    passed = sum(1 for v in results.values() if "✅" in v)
    total = len(results)

    print(f"\n總計: {passed}/{total} 通過\n")

    for ext, status in sorted(results.items()):
        print(f"  {status} {ext}")

    if failed_tests:
        print("\n" + "=" * 60)
        print("❌ 失敗的測試詳情")
        print("=" * 60)
        for test in failed_tests:
            print(f"\n語言: {test['ext']}")
            print(f"映像檔: {test['image']}")
            print(f"錯誤: {test['error'][:200]}")

        print("\n" + "=" * 60)
        print("❌ 有測試失敗！請檢查 core/runner.py 中的配置")
        print("=" * 60)
        return False
    else:
        print("\n" + "=" * 60)
        print("✅ 所有語言測試通過！")
        print("=" * 60)
        return True

if __name__ == "__main__":
    success = test_all_languages()
    sys.exit(0 if success else 1)
