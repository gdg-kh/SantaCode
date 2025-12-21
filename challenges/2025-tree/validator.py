import sys

def validate_tree(output_text):
    """
    簡單檢查 Output 是否像一棵樹
    1. 不可以是空的
    """
    if not output_text or not output_text.strip():
        return False, "Output is empty!"

    return True, "Tree output detected."

if __name__ == "__main__":
    # 從 stdin 讀取 output
    content = sys.stdin.read()
    valid, message = validate_tree(content)
    
    if valid:
        print(f"PASS: {message}")
        sys.exit(0)
    else:
        print(f"FAIL: {message}")
        sys.exit(1)

