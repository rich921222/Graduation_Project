import random
from skimage import io

def embeding(image,n):
    def noise(I,Noise):
        n_r,n_c = Noise.shape[0],Noise.shape[1]

        r_base = random.randint(0,I.shape[0]-n_r)
        c_base = random.randint(0,I.shape[1]-n_c)
        for i in range(n_r):
            for j in range(n_c):
                if(Noise[i, j,3]==0):
                    continue
                for k in range(3):
                    I[i+r_base,j+c_base,k] = Noise[i,j,k]

        return I
    path = "processing_image/"+image+".png"
    I=io.imread(path)
    path2 = "noise/"+n+".png"
    I2=io.imread(path2)
    e = noise(I,I2)
    # io.imshow(e)
    # io.show()
    io.imsave('embeding_noise/'+image+'.png',e)