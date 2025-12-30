fun main() {
    val messages = listOf(
        "2025.",
        "GDG Kaohsiung",
        "Marry Christmas",
        "Happy New Year.",
        "by Andy"
    )

    val totalWidth = 29  // 總寬度

    // 使用迴圈印出每一行
    for (i in messages.indices) {
        val starCount = i + 1  // 星號數量：1, 2, 3, 4, 5
        val message = messages[i]

        // 計算中間內容的寬度（扣除左右星號）
        val contentWidth = totalWidth - starCount * 2

        // 計算文字左右的空格數（讓文字置中）
        val leftPadding = (contentWidth - message.length) / 2
        val rightPadding = contentWidth - leftPadding - message.length

        // 組合並印出這一行
        val line = "${"*".repeat(starCount)}${" ".repeat(leftPadding)}${message}${" ".repeat(rightPadding)}${"*".repeat(starCount)}"

        println(line)
    }

    // 最後一行特殊處理
    println("▌" + " ".repeat(totalWidth - 2) + "▐")
}