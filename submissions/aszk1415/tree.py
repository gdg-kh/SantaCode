#!/usr/bin/env python3
"""SantaCode 2025 - Rocket Christmas Tree"""
import math

# ANSI colors
def rgb(r, g, b): return f"\033[38;2;{r};{g};{b}m"
RST = "\033[0m"

# 顏色
WHITE = rgb(255, 255, 255)
GOLD = rgb(255, 220, 50)
RED = rgb(255, 60, 60)
GREEN = rgb(50, 220, 100)
BLUE = rgb(100, 180, 255)
PINK = rgb(255, 120, 180)
CYAN = rgb(50, 220, 220)
PURPLE = rgb(200, 100, 255)
ORANGE = rgb(255, 150, 50)
BROWN = rgb(160, 100, 60)
YELLOW = rgb(255, 240, 100)

# 火焰顏色
FLAME = [
    rgb(255, 255, 220),
    rgb(255, 240, 100),
    rgb(255, 200, 50),
    rgb(255, 150, 0),
    rgb(255, 100, 0),
    rgb(220, 60, 0),
]

def rainbow(text, offset=0):
    result = ""
    for i, c in enumerate(text):
        h = ((i + offset) / max(len(text), 1)) % 1.0
        r = int(math.sin(h * 6.28) * 127 + 128)
        g = int(math.sin(h * 6.28 + 2.09) * 127 + 128)
        b = int(math.sin(h * 6.28 + 4.18) * 127 + 128)
        result += f"{rgb(r, g, b)}{c}"
    return result + RST

# 裝飾球顏色列表
ORNAMENT_COLORS = [RED, BLUE, GREEN, PINK, CYAN, PURPLE, GOLD]

def print_tree():
    W = 48  # 總寬度
    tree_height = 12
    
    # 計算樹頂位置 (第一層寬度=1, 所以中點位置)
    tree_center = W // 2
    
    # ═══════════════ 標題 ═══════════════
    border = "+" + "-" * (W - 2) + "+"
    print(f"{GOLD}{border}{RST}")
    title = "ROCKET CHRISTMAS TREE 2025"
    pad = (W - 2 - len(title)) // 2
    print(f"{GOLD}|{RST}{' ' * pad}{rainbow(title)}{' ' * (W - 2 - pad - len(title))}{GOLD}|{RST}")
    print(f"{GOLD}{border}{RST}")
    print()
    
    # ═══════════════ 星星 (直接連接樹頂) ═══════════════
    # 樹頂第一層寬度=1, 左邊空格 = (W-1)//2 = 23
    star_pad = (W - 1) // 2
    print(" " * star_pad + f"{YELLOW}*{RST}")       # 星星頂部
    print(" " * (star_pad - 1) + f"{YELLOW}/|\\{RST}")  # 星星連接
    
    # ═══════════════ 聖誕樹 ═══════════════
    orn_idx = 0
    
    for row in range(tree_height):
        tree_width = 1 + row * 2
        left_pad = (W - tree_width) // 2
        
        line = ""
        for i in range(tree_width):
            # 計算火焰強度（中心亮，邊緣暗）
            center = tree_width // 2
            dist = abs(i - center)
            fire_level = min(5, int(dist / max(center, 1) * 5))
            
            # 每隔幾個放裝飾球
            if row > 1 and i > 0 and i < tree_width - 1:
                if (i + row) % 4 == 0:
                    color = ORNAMENT_COLORS[orn_idx % len(ORNAMENT_COLORS)]
                    line += f"{color}o{RST}"
                    orn_idx += 1
                else:
                    line += f"{FLAME[fire_level]}*{RST}"
            else:
                line += f"{FLAME[fire_level]}*{RST}"
        
        print(" " * left_pad + line)
    
    # ═══════════════ 樹幹 ═══════════════
    trunk_width = 5
    trunk_pad = (W - trunk_width) // 2
    print(" " * trunk_pad + f"{BROWN}|||||{RST}")
    print(" " * trunk_pad + f"{BROWN}|||||{RST}")
    
    # ═══════════════ 推進器火焰 ═══════════════
    exhaust_widths = [9, 13, 17, 21, 13]
    for i, ew in enumerate(exhaust_widths):
        pad = (W - ew) // 2
        if i < 4:
            fire_level = min(5, i)
            line = f"{FLAME[fire_level]}{'#' * ew}{RST}"
        else:
            line = f"{FLAME[5]}{'.' * ew}{RST}"
        print(" " * pad + line)
    
    print()
    
    # ═══════════════ 禮物盒 ═══════════════
    box_start = (W - 35) // 2
    sp = " " * box_start
    
    print(f"{sp}{RED}+-------+{RST}    {ORANGE}+-------+{RST}    {PURPLE}+-------+{RST}")
    print(f"{sp}{RED}| {GOLD}GIFT{RED}  |{RST}    {ORANGE}| {GOLD}MERRY{ORANGE} |{RST}    {PURPLE}| {CYAN}XMAS{PURPLE}  |{RST}")
    print(f"{sp}{RED}|   {GOLD}*{RED}   |{RST}    {ORANGE}|   {GOLD}*{ORANGE}   |{RST}    {PURPLE}|   {CYAN}*{PURPLE}   |{RST}")
    print(f"{sp}{RED}+-------+{RST}    {ORANGE}+-------+{RST}    {PURPLE}+-------+{RST}")
    
    print()
    
    # ═══════════════ 地面 ═══════════════
    print(f"{FLAME[3]}{'=' * W}{RST}")
    print()
    
    # ═══════════════ 祝福語 ═══════════════
    msg1 = "Made with ROCKET FUEL for SantaCode 2025"
    msg2 = "Happy Holidays & Merry Christmas!"
    pad1 = (W - len(msg1)) // 2
    pad2 = (W - len(msg2)) // 2
    print(" " * pad1 + rainbow(msg1, 0))
    print(" " * pad2 + rainbow(msg2, 5))

if __name__ == "__main__":
    print_tree()
