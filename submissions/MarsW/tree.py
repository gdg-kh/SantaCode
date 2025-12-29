# https://zerojudge.tw/ShowProblem?problemid=q089

height = 25
width = height*2-1
# 樹冠
for h in range(1, height+1):
  base = "* "*(h-1) + "*"
  side_space = ((width-len(base))//2)*" "
  output = f"{side_space}{base}{side_space}"
  print(output)
# 樹幹
base = "| |"
side_space = ((width-len(base))//2)*" "
output = f"{side_space}{base}{side_space}" 
for i in range((height//2)):
  print(output)

# 盆栽
bottom = "_"*(width-2)
plat = f"\\{bottom}/"
print(plat)