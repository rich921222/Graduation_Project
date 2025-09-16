import Toollib as T
import numpy as np
from skimage import io
import pandas as pd

def AVGI(Graph):

    ## 引入圖片
    path = 'image/'+Graph
    I=io.imread(path +r'.tiff')
    Stego = I.copy()

    ## 嘗試是否有建立參照表
    try:
        df = pd.read_csv('RT.csv')
        RT_table = df.to_numpy()
    except:
        RT = T.APPM_RT256()
        df = pd.DataFrame(RT)
        df.to_csv('RT.csv', index=False, header=True)
        df = pd.read_csv('RT.csv')
        RT_table = df.to_numpy()

    NearestP = T.NearestPoint()

    p = 0
    MSE = 0
    F = 0
    N = 0
    delta_RB_List = []
    extra_bit = np.zeros((512,512))

    for i in range(Stego.shape[0]):
        for j in range(Stego.shape[1]):
            
            ## 計算灰階值並將其設為驗證碼
            Gray = I[i,j,0]*0.299+I[i,j,1]*0.587+I[i,j,2]*0.114
            G_round = round(Gray)
            ## 使用灰階值+索引做驗證碼(AC)
            ac = T.hashB(np.array([G_round,i,j]),8)    
            ac2 = T.hashB(np.array([G_round,i,j,32]),8) 
            
            ## 由參照表中依照順序(最近優先)尋找數值等於ac的點，並回傳其XY軸座標 -> k
            k = T.Find(RT_table,NearestP,Stego[i,j,0],Stego[i,j,2],ac)   
            k2 =  T.Find(RT_table,NearestP,Stego[i,j,0],Stego[i,j,2],ac2)         

            ## X座標放入紅色通道，Y座標放入藍色通道，並判斷綠色通道要變化成多少彌補灰階值 -> g_bar
            g_bar = int((Gray - 0.299*k[0] - 0.114*k[1])/0.587)
            g_bar2 = int((Gray - 0.299*k2[0] - 0.114*k2[1])/0.587)
            if(round(0.299*k[0]+0.587*g_bar+0.114*k[1]) < round(Gray)):
                g_bar += 1
            elif(round(0.299*k[0]+0.587*g_bar+0.114*k[1]) > round(Gray)):
                g_bar -= 1

            if(round(0.299*k2[0]+0.587*g_bar2+0.114*k2[1]) < round(Gray)):
                g_bar2 += 1
            elif(round(0.299*k2[0]+0.587*g_bar2+0.114*k2[1]) > round(Gray)):
                g_bar2 -= 1

            ## 若g_bar超過臨界值則進行折返
            if(g_bar > 255):
                p += 1
                g_bar = 510 - g_bar
            elif(g_bar < 0):
                p += 1
                g_bar = g_bar*-1
            
            if(g_bar2 > 255):
                g_bar2 = 510 - g_bar2
            elif(g_bar2 < 0):
                g_bar2 = g_bar2*-1
            
            if(((k[0]-Stego[i,j,0])**2+(k[1]-Stego[i,j,2])**2+(g_bar-Stego[i,j,1])**2)<((k2[0]-Stego[i,j,0])**2+(k2[1]-Stego[i,j,2])**2+(g_bar2-Stego[i,j,1])**2)):
                Stego[i,j,0] = k[0]
                Stego[i,j,2] = k[1]              
                Stego[i,j,1] = g_bar
            else:
                extra_bit[i,j] = 1
                Stego[i,j,0] = k2[0]
                Stego[i,j,2] = k2[1]              
                Stego[i,j,1] = g_bar2     

            ## 計算三個通道的變化平方和

            delta_B = int(Stego[i,j,2]) - int(I[i,j,2])
            MSE += delta_B ** 2
            ## 累計R或B變化量超過8的數量
            if(delta_B**2 > 64):
                N += 1

            delta_G = int(Stego[i,j,1]) - int(I[i,j,1])
            MSE += delta_G ** 2 

            delta_R = int(Stego[i,j,0]) - int(I[i,j,0]) 
            MSE += delta_R ** 2  
            if(delta_R**2 > 64 and delta_B**2 <= 64):
                N += 1   

            delta_RB_List.append((delta_R, delta_B))                                  
    
    ## 計算PSNR
    MSE /= (Stego.shape[0]*Stego.shape[1]*3)
    PSNR = 10 * np.log10(65025/MSE)
    print(f"PSNR:{PSNR} , 折返的Green:{p} , R或B變化量大於8:{N}")

    with open("processing_data/"+Graph+".txt","w") as file:
        file.write(f"PSNR: {PSNR}\n")
        file.write(f"outliers: {p}\n")
        file.write(f"The change is more than 8: {N}\n")

    # io.imshow(Stego)
    # io.show()
    io.imsave('processing_image/'+Graph+'.png',Stego)
    return delta_RB_List,extra_bit