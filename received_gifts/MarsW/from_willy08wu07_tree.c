#include <stdio.h>

int main() {
    int height = 10; // 樹的高度

    // 畫樹葉部分
    for (int i = 0; i < height; i++) {
        // 印出左側空格
        for (int j = 0; j < height - i - 1; j++) {
            printf(" ");
        }

        // 印出樹葉與裝飾
        for (int k = 0; k < (2 * i + 1); k++) {
            if (i == 0) {
                printf("★"); // 頂端的星星
            } else if (k % 3 == 0) {
                printf("o"); // 裝飾小球
            } else {
                printf("*"); // 一般樹葉
            }
        }
        printf("\n");
    }

    // 畫樹幹部分
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < height - 3; j++) {
            printf(" ");
        }
        printf("[___]\n");
    }

    return 0;
}
