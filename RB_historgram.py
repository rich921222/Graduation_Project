import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def RB_histogram_Variation_Frequency(delta_RB,image):
    delta_RB_ravel = delta_RB.ravel()
    delta_RB_ravel = np.abs(delta_RB_ravel)
    bins = range(0, 16)
    counts, edges = np.histogram(delta_RB_ravel, bins=bins)
    print(counts)
    path = "variation_csv/"+image+".csv"
    pd.DataFrame(delta_RB_ravel).to_csv(path, index=False, header=False)
    
    # 繪製長條圖
    plt.bar(edges[:-1], counts, width=1, edgecolor="black", align="edge")

    # 設置橫軸範圍和標籤
    plt.xticks(range(0, 16))
    plt.xlabel("Variation")
    plt.ylabel("number of pixels")
    plt.title("The variation of R or B channel")
    
    plt.savefig(f"Variation-Frequency/{image}_APPM.png")
    plt.clf()
    # 顯示圖表
    # plt.show()