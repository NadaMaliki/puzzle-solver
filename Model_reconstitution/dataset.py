import torch  # type: ignore
import pandas as pd  # type: ignore
import os 
import cv2 as cv  # type: ignore
from torch.utils import data as torch_data  # type: ignore
from PIL import Image # type: ignore


class JigsawDataset(torch_data.Dataset):
    """
    To reduce the preprocessing time, we have preprocessed the data first.
    The Dataset will output an Image and 9 Numbers corresponding to the position of the peices."""

    def __init__(self, df, root_dir, transform, num_piece=9):
        """
        Args: 
            df (pd.DataFrame): DataFrame with positions.
            root_dir (string): Path to the dir. where all images are present.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """

        self.df = df
        self.root_dir = root_dir
        self.transform = transform 
        self.num_piece =num_piece

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        """
        returns: a python dictionary containing the image and correct index.
        """
        img_name = str(self.df.iloc[idx, 0])
        img = cv.imread(os.path.join(self.root_dir, img_name))
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        d = {"img": img}
        for i in range(self.num_piece):
            d[f"perm{i}"] = self.df.iloc[idx, i+1]

        if self.transform is not None:
            d["img"] = self.transform(img)

        return d