# 原題：https://zerojudge.tw/ShowProblem?problemid=q089

import time
import random
import sys

# Define colors
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"
BROWN = "\033[38;5;94m"
COLORS = [YELLOW, BLUE, MAGENTA, CYAN, WHITE]
ORNAMENTS = ["o", "@", "*"]

height = 20
width = height * 2 - 1

for i in range(50):
    # \033[H moves cursor to home, \033[J clears from cursor to end of screen
    print("\033[H\033[J")

    ### 繪製樹冠
    for h in range(1, height + 1):
        leaf_content = []
        for i in range(h * 2 - 1):
            if i % 2 == 0:
                # 30% 機率出現彩色裝飾品，70% 是綠色樹葉
                if random.random() < 0.3:
                    color = random.choice(COLORS)
                    char = random.choice(ORNAMENTS)
                    leaf_content.append(f"{color}{char}{RESET}")
                else:
                    leaf_content.append(f"{GREEN}*{RESET}")
            else:
                leaf_content.append(" ")

        leaf = "".join(leaf_content)
        # 每一層的字元寬度是 (h*2-1)
        padding = " " * ((width - (h * 2 - 1)) // 2)
        print(f"{padding}{leaf}")


    ### 繪製樹幹 (棕色)
    trunk = "| |"
    trunk_padding = " " * ((width - len(trunk)) // 2)
    for _ in range(height // 4): # 顯示方便，修改成比原題矮
        print(f"{trunk_padding}{BROWN}{trunk}{RESET}")

    # 繪製盆栽
    pot = "_"*(width-2)
    print(f"\\{pot}/")

    sys.stdout.flush()
    time.sleep(0.5)
