import os 
import pandas as pd  # type: ignore
from tqdm import tqdm # type: ignore
from PIL import Image  # type: ignore
import numpy as np  # type: ignore
import random

np.random.seed(2020)
random.seed(2020)

data_dir = "data/imet-2020-fgvc7/train/"

df = pd.DataFrame(columns=["img_name", "1", "2", "3", "4", "5", "6", "7", "8", "9"]) 
save_dir_complete = "data/generated_data/"

file_list = os.listdir(data_dir)
file_list = random.sample(file_list, min(len(file_list), 45000))

for i in tqdm(file_list):
    img_name = i
    img = Image.open(os.path.join(data_dir, i))
    h = img.height
    w = img.width
    h = h - h%3
    w = w - w%3
    h_3 = h//3
    w_3 = w//3
    h_2 = int((2/3)*h)
    w_2 = int((2/3)*w)
    img  = np.array(img)

    if len(img.shape) == 3:
        rand_perm = np.random.permutation(9)
        img_dict = {
            1: img[0: h_3, 0: w_3, :], 
            2: img[0: h_3, w_3: w_2, :], 
            3: img[0: h_3 , w_2: w, :],
            4: img[h_3:h_2 , 0: w_3, :],
            5: img[h_3:h_2 , w_3: w_2, :], 
            6: img[h_3:h_2 , w_2: w, :], 
            7: img[h_2:h , 0: w_3, :], 
            8: img[h_2:h , w_3: w_2, :],
            9: img[h_2:h , w_2: w, :],
        }

        zeros = np.zeros(shape= (h, w, 3), dtype= np.uint8)
        k = 0

        l = [0,0,0,1,1,1,2,2,2]
        m= [0, w_3, w_2, 0, w_3, w_2,  0, w_3, w_2]
        for g in rand_perm:
            zeros[l[k]*h_3 : h_3*(l[k] + 1), m[k]: w_3*(k%3 + 1), :] = img_dict[g+1]
            k = k+1

        img_converted = Image.fromarray(zeros, "RGB")
        
    if len(img.shape) == 2:
        rand_perm = np.random.permutation(9)
        img_dict = {
            1: img[0: h_3, 0: w_3], 
            2: img[0: h_3, w_3: w_2], 
            3: img[0: h_3 , w_2: w],
            4: img[h_3:h_2 , 0: w_3],
            5: img[h_3:h_2 , w_3: w_2], 
            6: img[h_3:h_2 , w_2: w], 
            7: img[h_2:h , 0: w_3], 
            8: img[h_2:h , w_3: w_2],
            9: img[h_2:h , w_2: w],
        }

        zeros = np.zeros(shape= (h, w), dtype= np.uint8)
        k = 0

        l = [0,0,0,1,1,1,2,2,2]
        m= [0, w_3, w_2, 0, w_3, w_2,  0, w_3, w_2]
        for g in rand_perm:
            zeros[l[k]*h_3 : h_3*(l[k] + 1), m[k]: w_3*(k%3 + 1)] = img_dict[g+1]
            k = k+1

        img_converted = Image.fromarray(zeros, "L")
            
    img_converted.save(os.path.join(save_dir_complete, img_name))
    df = df.append({"img_name": img_name,
                   "1": rand_perm[0],
                   "2": rand_perm[1], 
                   "3": rand_perm[2],
                   "4": rand_perm[3], 
                   "5": rand_perm[4], 
                   "6": rand_perm[5], 
                   "7": rand_perm[6], 
                   "8": rand_perm[7], 
                   "9": rand_perm[8]}, ignore_index=True)

df.to_csv("data/met_permuted.csv")
