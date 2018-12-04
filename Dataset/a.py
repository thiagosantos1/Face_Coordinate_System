
fd = open('x.ppm','r')
li = fd.readlines()
k = 0
print('P2')
print(li[1],end='')
print(li[2],end='')
for line in li[3:]:
  lj = list(map(int,line.split()))
  for x in lj:
    if k % 3 == 0:
      print(x)
    k += 1
