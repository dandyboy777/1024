from icecream import ic
import random
import curses
import time

def inpdig(min,max):
  while True:
    k=input()
    if k=="q":
      exit(0)
    try:
      if (int(k)) in range((min),(max+1)):
        return int(k)
    except:
      continue



ic.configureOutput(prefix='')
maingrid=[]
N=5
MINrange=1
MAXrange=4
nex_newdig=2

MINmaingrid=1
MIN_DIF_MIX_MAX_range=3
MAXmaingrid=MINmaingrid+MIN_DIF_MIX_MAX_range
PAUSE=0.2
maingrid=[[0]*N for i in range (N)]

def find_min():
  min_maingrid=maingrid[0][0]
  for i in range(N):
    for j in range(N):
      if maingrid[i][j]:
        if  maingrid[i][j]<min_maingrid:
          min_maingrid=maingrid[i][j]
  return min_maingrid

def printM():
  for i in range(N):
    for j in range(N):
      if maingrid[i][j]==0:
        print("|    ",end="") 
      elif maingrid[i][j]<10:
        print("|{:4d}".format(2**maingrid[i][j]),end="")
      elif maingrid[i][j]<20:
        print("|{:3d}K".format(2**(maingrid[i][j]-10)),end="")
      elif maingrid[i][j]<30:
        print("|{:3d}M".format(2**(maingrid[i][j]-10)),end="")
    print("|")
  for i in range(N):
     print("-"*5,end="")
  print("-")

# проходим по все таблице и смещаем все ненулевые ячейки перед которыми есть нулевая ячейка
def shift(ki,kj):
  fl=False
  fl2=True
  for i in range(N-1):
    for j in range(N):
      while maingrid[i][j]==0 and maingrid[i+1][j]!=0 and (i+1):
        maingrid[i][j]=maingrid[i+1][j]
        maingrid[i+1][j]=0
        ki,kj=i,j
        i-=1
        fl=True
      if fl:
        fl=False
        fl2=False
        printM()
        time.sleep(PAUSE)  
        while add_cells(ki,kj):
          shift(ki,kj)
  if fl2:
    printM()
    while add_cells(ki,kj):
      shift(ki,kj)

def search_identical_cells(ki, kj, k):
  i,j=ki,kj
  k.append((ki,kj))
  mem=maingrid[ki][kj]
  maingrid[ki][kj]=0
  # проверяем ячейки вверх
  while i>0 and maingrid[i-1][j]==mem:
      search_identical_cells(i-1,j,k)
      i-=1
  i,j=ki,kj
  
  # проверяем ячейки вниз
  while i+1<N and maingrid[i+1][j]==mem:
     search_identical_cells(i+1,j,k)
     i+=1
  i,j=ki,kj
 # проверяем ячейки влево
  while j>0 and maingrid[i][j-1]==mem:
     search_identical_cells(i,j-1,k)
     j-=1
  i,j=ki,kj
   # проверяем ячейки вправо
  while j+1<N and maingrid[i][j+1]==mem:
     search_identical_cells(i,j+1,k)
     j+=1

#проверяем соседние ячейки и складываем соседние если их значения равны и заменяем их нулями
def add_cells(ki,kj):
  if maingrid[ki][kj]==0:
    return 0

  mem=maingrid[ki][kj]
  # находим последовательности во все стороны. сохраняем их и затем все сложим
  k=[]
  k.append((ki,kj))
  search_identical_cells(ki,kj,k)
  k=list(dict.fromkeys(k)) # убираем дубликаты

  maingrid[ki][kj]=mem+len(k)-1
  if (len(k)-1)>0:
    printM()
    time.sleep(PAUSE)

  return len(k)-1

def check_end_game():
  # проверяем настал ли конец игры
  for j in range(N):
    if maingrid[N-1][j]==0:
      break
  else:
    print("Конец!")
    return 1
  return 0


printM()
while True:
  newdig=nex_newdig
  nex_newdig = random.randint(MINrange,MAXrange)
  
  while True:
    print("New:{:d} Next:{:d} Max:{:d} Minr:{:d} Maxr:{:d}".format(2**newdig,2**nex_newdig,2**MAXmaingrid,2**MINrange,2**MAXrange))
    
   
    clmn=((inpdig(1,5))%N)-1
    
    
    if maingrid[N-1][clmn]:
      if maingrid[N-1][clmn]!=newdig:
        print("!")
        continue
    break
  if maingrid[N-1][clmn]==newdig:
    maingrid[N-1][clmn]+=1
    while add_cells(N-1,clmn):
      printM()
      shift(N-1,clmn)
    else:
      printM()
    
  else:
    maingrid[N-1][clmn]=newdig
    shift(N-1,clmn)
    # ic(max(maingrid))
  if MAXmaingrid<max(max(maingrid))-1:
    MAXmaingrid=max(max(maingrid))-1
    print("New max")
    if MAXmaingrid > MAXrange:
      MAXrange+=1
  if find_min()>MINrange and (MAXrange-MINrange)>MIN_DIF_MIX_MAX_range:
    MINrange+=1
    print("New min")
  if check_end_game():
    break
