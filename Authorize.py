import Toollib as T
import numpy as np
from skimage import io
import pandas as pd

def Authorize(Graph,extra_bit):
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
    
    ## 匯入圖片
    path = "embeding_noise/"+Graph+".png"
    I=io.imread(path)
    Stego = I.copy()
    Flag = False

    ## 檢測圖片是否遭到竄改
    detected_error = 0
    diff_pixels = 0
    for i in range(Stego.shape[0]):
        for j in range(Stego.shape[1]):

            ## 計算灰階值
            Gray = I[i,j,0]*0.299+I[i,j,1]*0.587+I[i,j,2]*0.114
            G_round = round(Gray)
            if(extra_bit[i,j] == 0):
                ac =  T.hashB(np.array([G_round,i,j]),8)
            else:
                ac =  T.hashB(np.array([G_round,i,j,32]),8)

            flag = False
            ## 若灰階值大於驗證碼，則查看是否是因為折返導致
            if(ac != RT_table[Stego[i,j,0],Stego[i,j,2]]):
                if(I[i,j,1] > 240):
                    Gray = I[i,j,0]*0.299+(510-I[i,j,1])*0.587+I[i,j,2]*0.114
                elif(I[i,j,1] < 15):
                    Gray = I[i,j,0]*0.299+(-1*I[i,j,1])*0.587+I[i,j,2]*0.114
                G_round = round(Gray)
                if(extra_bit[i,j] == 0):
                    ac =  T.hashB(np.array([G_round,i,j]),8)
                else:
                    ac =  T.hashB(np.array([G_round,i,j,32]),8)
                if(ac != RT_table[Stego[i,j,0],Stego[i,j,2]]):
                    Stego[i,j,0] = 255
                    Stego[i,j,1] = 255
                    Stego[i,j,2] = 255
                    flag = True
                    detected_error += 1
                    # print(f"This picture is tampered. i: {i} ,j: {j} ,Stego:{Stego[i,j]} ,Gray:{Gray}, RT_table:{RT_table[Stego[i,j,0],Stego[i,j,2]]}")
                    # Flag = True
                    # break 
            if(not flag):
                Stego[i,j,0] = 0
                Stego[i,j,1] = 0
                Stego[i,j,2] = 0
                
    # io.imshow(Stego, vmin=0, vmax=255)
    # io.show()
    io.imsave('result_image/'+Graph+'.png',Stego)  
    image1 = io.imread("embeding_noise/"+Graph+".png")
    image2 = io.imread('processing_image/'+Graph+'.png')
    
    for i in range(image1.shape[0]):
        for j in range(image1.shape[1]):
            if(image1[i,j] != image2[i,j]).any():
               diff_pixels+=1 
    # print(Graph)
    accuracy = detected_error/diff_pixels
    print(f"Detected error: {detected_error}, Actual error: {diff_pixels}, Accuracy: {accuracy}")

    with open("processing_data/"+Graph+".txt","a") as file:
        file.write(f"accuracy: {accuracy}\n")    
    return accuracy