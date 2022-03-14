import copy
_list=list(open("wordlist2.txt").read().splitlines())
_list.sort(key=len, reverse=True)

height=5
width=5
maxoverlap=1
symmetry=True
grid=[['0']*width for i in range(height)]

def cprint(grid):
    print('\n'.join([''.join(['{:3}'.format(item) for item in row]) 
      for row in grid]))

def findvalids(word,grid):
    valids=[]
    for i in range(0,len(grid[0])-len(word)+1):
        for j in range(0,len(grid)):
            testvalid = True
            for k in range(0,len(word)):
                if grid[j][i+k] != '0' and grid[j][i+k] != word[k]:
                    testvalid = False
                    break
            for k in range(maxoverlap,len(word)-maxoverlap-1):
                if j > 0:
                    if grid[j-1][i+k] != '0' and grid[j-1][i+k+1] != '0':
                        testvalid = False
                        break
                    if symmetry:
                        if grid[-j][-i-k-1] != '0' and grid[-j][-i-k-2] != '0':
                            testvalid = False
                            break

                if j<len(grid)-1:
                    if grid[j+1][i+k] != '0' and grid[j+1][i+k+1] != '0':
                        testvalid = False
                        break
                    if symmetry:
                        if grid[-j-2][-i-k-1] != '0' and grid[-j-2][-i-k-2] != '0':
                            testvalid = False
                            break
            if i>0:
                if grid[j][i-1] not in ['0',' ']:
                    testvalid = False
                if symmetry:
                    if grid[-j-1][-i] not in ['0',' ']:
                        testvalid = False
            if i+len(word)<len(grid[0]):
                if grid[j][i+len(word)] not in ['0',' ']:
                    testvalid = False
                if symmetry:
                    if grid[-j-1][-i-len(word)-1] not in ['0',' ']:
                        testvalid = False
            
            if symmetry and j*2+1==len(grid) and 2*len(word)>=len(grid[0]) and len(word) != len(grid[0]):
                testvalid = False
            
            if testvalid == True:
                valids.append([i,j,'Across'])

    for i in range(0,len(grid[0])):
        for j in range(0,len(grid)-len(word)+1):
            testvalid = True
            for k in range(0,len(word)):
                if grid[j+k][i] != '0' and grid[j+k][i] != word[k]:
                    testvalid = False
                    break
            for k in range(maxoverlap,len(word)-maxoverlap-1):
                if i > 0:
                    if grid[j+k][i-1] != '0' and grid[j+k+1][i-1] != '0':     
                        testvalid = False
                        break
                    if symmetry:
                        if grid[-j-k-1][-i] != '0' and grid[-j-k-2][-i] != '0':     
                            testvalid = False
                            break

                if i<len(grid[0])-1:
                    if grid[j+k][i+1] != '0' and grid[j+k+1][i+1] != '0':
                        testvalid=False
                        break
                    if symmetry:
                        if grid[-j-k-1][-i-2] != '0' and grid[-j-k-2][-i-2] != '0':
                            testvalid=False
                            break

            if j>0:        
                if grid[j-1][i] not in ['0',' ']:
                    testvalid = False
                if symmetry:
                    if grid[-j][-i-1] not in ['0',' ']:
                        testvalid = False

            if j+len(word)<len(grid):   
                if grid[j+len(word)][i] not in ['0',' ']:
                    testvalid = False
                if symmetry:
                    if grid[-j-len(word)-1][-i-1] not in ['0',' ']:
                        testvalid = False

            if symmetry and i*2+1==len(grid[0]) and 2*len(word)>=len(grid) and len(word)!=len(grid):
                testvalid = False

            if testvalid == True:
                valids.append([i,j,'Down'])
    return valids

def putin(word,grid,i,j,angle):
    if angle == 'Across':
        for k in range(0,len(word)):
            grid[j][i+k]=word[k]
        if i > 0:
            grid[j][i-1]=' '
            if symmetry == True:
                grid[-j-1][-i]=' '
        if i+len(word)<len(grid[0]):
            grid[j][i+len(word)]=' '
            if symmetry == True:
                grid[-j-1][-i-len(word)-1]=' '
    if angle == 'Down':
        for k in range(0,len(word)):
            grid[j+k][i]=word[k]
        if j > 0:
            grid[j-1][i]=' '
            if symmetry == True:
                grid[-j][-i-1]=' '
        if j+len(word)<len(grid):
            grid[j+len(word)][i]=' '
            if symmetry == True:
                grid[-j-len(word)-1][-i-1]=' '



def fill(grid,words,score):
    global bestscore
    #print(words)   
    if len(words)!=0:
        valids=findvalids(words[0],grid)
        for valid in valids:
            ngrid=copy.deepcopy(grid)
            nscore=score
            putin(words[0],ngrid,*valid)
            nscore+=1
            #cprint(ngrid)
            if nscore>=bestscore:
                bestscore=nscore
                cprint(ngrid)
                print(bestscore)
            nwords=list(words)
            nwords.pop(0)
            fill(ngrid,nwords,nscore)
        words.pop(0)
        fill(grid,words,score)
    else:
        return
    

if __name__=="__main__":
    score=0
    bestscore=0
    fill(grid,_list,score)