fun main() {
    val hiohAGoaKoan = 12
    val chhiuSinGoaChhoo = hiohAGoaKoan / 3
    val chhiuSinGoaKoan = hiohAGoaKoan / 5
    val chiokHokEOe = "Sèng-tàn-cheh Kiong-hí!"
    
    // 1. Ōe chhiū-hio̍h
    for (i in 1..hiohAGoaKoan) {
        val hiohAKhangPeh = " ".repeat(hiohAGoaKoan - i)
        val hiohA = "*".repeat(2 * i - 1)
        println("$hiohAKhangPeh$hiohA")
    }
    
    // 2. Ōe chhiū-sin
    val chhiuSinKhangPeh = " ".repeat(((2 * hiohAGoaKoan - 1) - chhiuSinGoaChhoo) / 2)
    repeat(chhiuSinGoaKoan) {
        println("$chhiuSinKhangPeh" + "#".repeat(chhiuSinGoaChhoo))
    }
    
    // 3. Siá jī chò thô͘-kha
    val thooKhaKhangPeh = " ".repeat(((2 * hiohAGoaKoan - 1) - chiokHokEOe.length) / 2)
    println("$thooKhaKhangPeh" + chiokHokEOe)
}