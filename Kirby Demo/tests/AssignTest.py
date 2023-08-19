fullscreen = ["A","B","C"]
newlist = ["D","E","F"]
fs1 = []
fs2 = []
fs3 = []
for item in fullscreen:
    fs1.append(item)
    fs2.append(item)
    fs3.append(item)
fullscreen = []
for item in newlist:
    fs1.insert(0,item)
fs2 =[1,2,3]
fs1[0] = "Vibri"
print(fs1,fs2,fs3)
