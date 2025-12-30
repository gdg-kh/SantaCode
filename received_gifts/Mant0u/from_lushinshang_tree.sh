#!/bin/sh
# tree.sh - SantaCode 2025 最終版
# 功能：
#   - 終端動畫聖誕樹（逐層出現、飾品閃爍、頂端星星）
#   - 底部祝福逐段顯示
#   - 最後2秒有流星動畫，流星頭旁顯示「陪你去看流星雨」
#   - 全程自動時長控制，確保4秒內結束
#   - POSIX相容，無第三方工具

# ----------- 資源清理與 trap -----------
cleanup() {
  # 還原游標與顏色
  printf "\033[?25h\033[0m"
  # 刪除暫存檔（存放飾品座標）
  [ -n "$ORN_FILE" ] && [ -f "$ORN_FILE" ] && rm -f "$ORN_FILE"
}

# INT/TERM 直接 exit，EXIT 只 cleanup
trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM
trap 'cleanup' EXIT

# ----------- 畫面初始化 -----------
printf "\033[2J\033[?25l" # 清屏並隱藏游標

# ----------- 參數區（可調整） -----------
# 終端自動偵測尺寸，無則 fallback
if command -v tput >/dev/null 2>&1; then
  cols=$(tput cols 2>/dev/null || echo 60)
  rows=$(tput lines 2>/dev/null || echo 16)
else
  cols=60
  rows=16
fi
max=8 # 樹層數

# 時序參數
TARGET_TOTAL=4         # 目標總時長（秒）
LAYER_DELAY=0.04       # 每層出現延遲（秒）
CHAR_DELAY=0.04        # 祝福逐段延遲（秒）
BLINK_INTERVAL=0.25    # 飾品/流星閃爍間隔（秒）

# ----------- 飾品暫存檔 -----------
ORN_FILE=$(mktemp 2>/dev/null || echo /tmp/tree_orn.$$)
rm -f "$ORN_FILE"
touch "$ORN_FILE"

# ----------- 聖誕樹動畫 -----------
# 逐層繪製樹身，並記錄飾品座標到暫存檔
level=1
while [ "$level" -le "$max" ]; do
  stars=$((2*level-1))
  row=$((level+3))
  col=$((cols/2 - level + 1))
  printf "\033[%s;%sH\033[32m" "$row" "$col" # 定位到該層
  j=0
  while [ "$j" -lt "$stars" ]; do
    # 飾品分布規則：每6格一個，顏色紅黃藍交錯
    t=$(( (j + level) % 6 ))
    if [ "$t" -eq 0 ]; then
      base=$((31 + (j % 3)))
      printf "\033[1;${base}mo\033[32m"
      printf '%s\n' "${row}:$((col+j)):${base}" >> "$ORN_FILE"
    else
      printf "#"
    fi
    j=$((j+1))
  done
  sleep $LAYER_DELAY
  level=$((level+1))
done

# ----------- 樹幹 -----------
tr=$((max+5)); tc=$((cols/2 - 2))
printf "\033[%s;%sH\033[33m[###]\033[0m" "$tr" "$tc"
printf "\033[%s;%sH\033[33m[###]\033[0m" "$((tr+1))" "$tc"

# ----------- 祝福逐段動畫 -----------
segments='阿星祝大家 聖誕快樂 ＆ 新年快樂'
msg_row=$((rows+3))
shown=""
for seg in $segments; do
  # 疊加片語，逐段顯示
  if [ -z "$shown" ]; then
    shown="$seg"
  else
    shown="$shown $seg"
  fi
  printf "\033[%s;1H\033[1;35m%s\033[0m" "$msg_row" "$shown"
  sleep $CHAR_DELAY
done

# ----------- 樹頂星星 -----------
top_row=$((1+3))
top_col=$((cols/2))
printf "\033[%s;%sH\033[1;33m★\033[0m" "$top_row" "$top_col"

# ----------- 飾品閃爍＋流星動畫 -----------
# 用 date 控制總時長，確保4秒內結束
t=0
start_time=$(date +%s)
while :; do
  now=$(date +%s)
  elapsed=$((now - start_time))
  if [ "$elapsed" -ge "$TARGET_TOTAL" ]; then
    break
  fi
  # 飾品閃爍（顏色紅黃藍交錯）
  while IFS= read -r item; do
    [ -z "$item" ] && continue
    row=${item%%:*}; rest=${item#*:}; col=${rest%%:*}; base=${rest#*:}
    color=$((31 + (t % 3)))
    printf "\033[%s;%sH\033[1;${color}mo\033[0m" "$row" "$col"
  done < "$ORN_FILE"

  # 最後2秒流星動畫（斜線閃過，頭部顯示文字）
  if [ "$elapsed" -ge $((TARGET_TOTAL-2)) ]; then
    meteor_len=6 # 流星長度
    for m in $(seq 0 $((meteor_len-1))); do
      m_row=$((2+m))
      m_col=$((4+m+t))
      printf "\033[%s;%sH\033[1;33m*\033[0m" "$m_row" "$m_col" # 流星本體
      # 流星頭旁顯示文字
      if [ "$m" -eq $((meteor_len-1)) ]; then
        txt_col=$((m_col+2))
        printf "\033[%s;%sH\033[1;36m陪你去看流星雨\033[0m" "$m_row" "$txt_col"
      fi
    done
  fi

  t=$((t+1))
  sleep $BLINK_INTERVAL
done

# ----------- 結尾祝福與清理 -----------
printf "\033[%s;1H\033[1;33m  阿星祝大家聖誕快樂＆新年快樂  \033[0m\n" $((rows+4))
cleanup
exit 0

cleanup() {
  # 只做還原工作（不要在 cleanup 裡再呼叫 exit）
  printf "\033[?25h\033[0m"
  # 移除暫存檔（若存在）
  [ -n "$ORN_FILE" ] && [ -f "$ORN_FILE" ] && rm -f "$ORN_FILE"
}

trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM
trap 'cleanup' EXIT

printf "\033[2J\033[?25l"

# ===== 可調參數 =====
# 嘗試自動偵測終端大小，無法取得時 fallback
if command -v tput >/dev/null 2>&1; then
  cols=$(tput cols 2>/dev/null || echo 60)
  rows=$(tput lines 2>/dev/null || echo 16)
else
  cols=60
  rows=16
fi
max=8

# timing（用 centiseconds 做計算）
TARGET_TOTAL=4
TARGET_TOTAL_CS=$((TARGET_TOTAL * 100))
LAYER_DELAY_CS=4      # 0.04s
CHAR_DELAY_CS=4       # 0.04s（每段）
BLINK_INTERVAL_CS=100 # 1s（避免小數 sleep）

# sleep 用的浮點字串（供 sleep 使用）
LAYER_DELAY=0.04
CHAR_DELAY=0.04
BLINK_INTERVAL=1

# 使用暫存檔儲存飾品，避免變數內換行/解析問題
ORN_FILE=$(mktemp 2>/dev/null || echo /tmp/tree_orn.$$)
rm -f "$ORN_FILE"
touch "$ORN_FILE"

# 1) 逐層繪製聖誕樹（由上而下），並記錄飾品位置
level=1
while [ "$level" -le "$max" ]; do
  stars=$((2*level-1))
  row=$((level+3))
  col=$((cols/2 - level + 1))
  printf "\033[%s;%sH\033[32m" "$row" "$col"
  j=0
  while [ "$j" -lt "$stars" ]; do
    # 以 j 與 level 決定飾品位置，確保飾品只在樹身內且分布均勻
    t=$(( (j + level) % 6 ))
    if [ "$t" -eq 0 ]; then
      base=$((31 + (j % 3)))
      printf "\033[1;${base}mo\033[32m"
      printf '%s\n' "${row}:$((col+j)):${base}" >> "$ORN_FILE"
    else
      printf "#"
    fi
    j=$((j+1))
  done
  sleep $LAYER_DELAY
  level=$((level+1))
done

# 2) 畫樹幹（靜態）
tr=$((max+5)); tc=$((cols/2 - 2))
printf "\033[%s;%sH\033[33m[###]\033[0m" "$tr" "$tc"
printf "\033[%s;%sH\033[33m[###]\033[0m" "$((tr+1))" "$tc"

# 3) 底部逐段顯示祝福（避免直接逐字切 UTF-8）
segments='阿星祝大家 聖誕快樂 ＆ 新年快樂'
msg_row=$((rows+3))
shown=""
for seg in $segments; do
  if [ -z "$shown" ]; then
    shown="$seg"
  else
    shown="$shown $seg"
  fi
  printf "\033[%s;1H\033[1;35m%s\033[0m" "$msg_row" "$shown"
  sleep $CHAR_DELAY
done

# 4) 在樹頂掛上黃色 Unicode 星號（★）
top_row=$((1+3))
top_col=$((cols/2))
printf "\033[%s;%sH\033[1;33m★\033[0m" "$top_row" "$top_col"

# ===== 計算閃爍次數（以避免使用 awk/bc） =====
segments_count=0
for _ in $segments; do segments_count=$((segments_count+1)); done
planned_cs=$((LAYER_DELAY_CS * max + CHAR_DELAY_CS * segments_count))
blink_dur_cs=$((TARGET_TOTAL_CS - planned_cs))
if [ "$blink_dur_cs" -lt 30 ]; then blink_dur_cs=30; fi
iterations=$((blink_dur_cs / BLINK_INTERVAL_CS))

# 5) 閃爍飾品（用換行分隔的 ORN_LIST 逐行讀取）
t=0
start_time=$(date +%s)
while :; do
  now=$(date +%s)
  elapsed=$((now - start_time))
  if [ "$elapsed" -ge "$TARGET_TOTAL" ]; then
    break
  fi
  # 標準飾品閃爍
  while IFS= read -r item; do
    [ -z "$item" ] && continue
    row=${item%%:*}; rest=${item#*:}; col=${rest%%:*}; base=${rest#*:}
    color=$((31 + (t % 3)))
    printf "\033[%s;%sH\033[1;${color}mo\033[0m" "$row" "$col"
  done < "$ORN_FILE"

  # 最後2秒流星動畫
  if [ "$elapsed" -ge $((TARGET_TOTAL-2)) ]; then
    # 流星座標：從左上到右下，座標依 t 變化
    meteor_len=6
    for m in $(seq 0 $((meteor_len-1))); do
      m_row=$((2+m))
      m_col=$((4+m+t))
      printf "\033[%s;%sH\033[1;33m*\033[0m" "$m_row" "$m_col"
      # 只在流星頭旁顯示文字
      if [ "$m" -eq $((meteor_len-1)) ]; then
        txt_col=$((m_col+2))
        printf "\033[%s;%sH\033[1;36m陪你去看流星雨\033[0m" "$m_row" "$txt_col"
      fi
    done
  fi

  t=$((t+1))
  sleep $BLINK_INTERVAL
done

# 結尾：再次印出祝福，還原游標並結束
printf "\033[%s;1H\033[1;33m  阿星祝大家聖誕快樂＆新年快樂  \033[0m\n" $((rows+4))
cleanup
exit 0

