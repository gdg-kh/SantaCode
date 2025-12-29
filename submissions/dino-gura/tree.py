def draw_dino_gura_santa_tree():
    # 這是聖誕樹與恐龍的 ASCII Art
    art = [
        "           * ",
        "          / \\          ",
        "         /   \\         ",
        "        / [o] \\        ",
        "       /_______\\       ",
        "        /     \\        ",
        "       /  ^ ^  \\       ",
        "      |  ( o_o ) |      ",
        "      |    -     |      ",
        "       \\_______/       ",
        "      /    |    \\      ",
        "   +-+-----+-----+-+   ",
        "   |               |   ",
        "   +---------------+   "
    ]

    for line in art:
        print(line)

if __name__ == "__main__":
    # 執行繪製函數
    draw_dino_gura_santa_tree()
