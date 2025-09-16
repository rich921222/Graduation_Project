import numpy as np

def Find(RT,NP,r,b,g):
    for i in range(len(NP)):
        if(r+NP[i,0] > 255 or r+NP[i,0] < 0):
            continue
        if(b+NP[i,1] > 255 or b+NP[i,1] < 0):
            continue        
        if(RT[r+NP[i,0],b+NP[i,1]] == g):
            return np.array([r+NP[i,0],b+NP[i,1]])