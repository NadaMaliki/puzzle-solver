import torch  # type: ignore
from torch import nn # type: ignore
import torch.optim as optim # type: ignore
from model import JigSolver
from dataset import *
from tqdm import tqdm # type: ignore
from torchvision import transforms # type: ignore
import torch.backends.cudnn as cudnn # type: ignore
from torch.utils import data as torch_data  # type: ignore
import random 
import numpy as np  # type: ignore
import pandas as pd # type: ignore
import os 
import time 
from sklearn.model_selection import train_test_split # type: ignore
import copy
import logging
import warnings
warnings.filterwarnings("ignore")

SEED = 2020

cudnn.benchmark = False
cudnn.deterministic = True
random.seed(SEED)
np.random.seed(SEED+1)
torch.manual_seed(SEED+2)
torch.cuda.manual_seed_all(SEED+3)


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")



composed_transform = transforms.Compose([
   transforms.Resize((350, 350)),
   transforms.ToTensor(),
   transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),])


train = pd.read_csv("./data/met_permuted.csv")
train = train.iloc[:, 1:]
X_train, X_val = train_test_split(train, test_size= .2, random_state = 2020, shuffle= True)
img_dir_path = "./data/generated_data/"
train_dataset = JigsawDataset(df = X_train,
                              root_dir=img_dir_path,
                              transform=composed_transform)
val_dataset = JigsawDataset(df = X_val, 
                           root_dir=img_dir_path,
                           transform=composed_transform)

trainloader = torch_data.DataLoader(train_dataset, batch_size= 16, shuffle=True)
valloader = torch_data.DataLoader(val_dataset, batch_size= 16, shuffle=False)

dataloaders = {"train": trainloader, 
               "val": valloader}
dataset_sizes = {"train":  len(train_dataset), 
                 "val": len(val_dataset)}


def train(num_epochs, model, optimizer, criterion, num_piece = 9):
   since = time.time()
   best_model_wts  = copy.deepcopy(model.state_dict())
   
   running_loss_train = []
   running_loss_val = []
   running_corrects_train = []
   running_corrects_val = []
   epoch_acc_hist = {"train": [], "val": []}
   epoch_loss_hist = {"train": [], "val": []}

   min_loss = 9999999

   for epoch in range(num_epochs):
      print(f"Epoch {epoch}/{num_epochs}")
      print("-"*15)

      for phase in ["train", "val"]:
         if phase == "train":
            model.train()
         else:
            model.eval()

         running_loss = 0.0
         running_corrects = 0.0

         for batch_idx, batch_data in enumerate(tqdm(dataloaders[phase])):
            inputs = batch_data["img"].to(device)
            for i in range(num_piece):
               # print(batch_data[f"perm{i}"])
               batch_data[f"perm{i}"] = batch_data[f"perm{i}"].to(device).long()

            model.zero_grad()

            with torch.set_grad_enabled(phase == "train"):
               out = model(inputs)
               batch_loss = 0.0
               for i in range(num_piece):
                  batch_loss += criterion(out[i], batch_data[f"perm{i}"])

               if phase == "train":
                  batch_loss.backward()
                  optimizer.step()

            running_loss += batch_loss*inputs.size(0)
            if phase == "train":
               running_loss_train.append(batch_loss.item())
            elif phase == "val":
               running_loss_val.append(batch_loss.item())

            batch_corrects = 0.0
            for i in range(num_piece):
               batch_corrects += torch.sum((torch.max(out[i], 1))[1] == batch_data[f"perm{i}"].data)
            batch_corrects = batch_corrects.double()/num_piece
            running_corrects += batch_corrects
            if phase == "train":
               running_corrects_train.append(batch_corrects.item())
            elif phase == "val":
               running_corrects_val.append(batch_corrects.item())

         epoch_loss = running_loss / len(dataloaders[phase].dataset)
         epoch_acc = running_corrects / len(dataloaders[phase].dataset)
         epoch_acc_hist[phase].append(epoch_acc)
         epoch_loss_hist[phase].append(epoch_loss)


         print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))

         if phase == "val" and epoch_loss < min_loss:
            min_loss = epoch_loss
            best_model_wts = copy.deepcopy(model.state_dict())

         if phase == "val":
            torch.save({"current_model_wts": model.state_dict(),
                        "best_model_wts": best_model_wts,
                        "current_epoch": epoch,
                        "optimizer_wts": optimizer.state_dict(),
                        "running_loss_train": running_loss_train, 
                        "running_loss_val": running_loss_val, 
                        "running_corrects_train": running_corrects_train,
                        "running_corrects_val": running_corrects_val,
                        "epoch_acc_hist": epoch_acc_hist,
                        "epoch_loss_hist":epoch_loss_hist, }, 
                        "28-09-2020_06-07.pth")

   time_elapsed = time.time() - since
   print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
   print('Min val Loss: {:4f}'.format(min_loss))                  


model = JigSolver().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr= 0.0001, ) # add weight decay
train(15, model, optimizer, criterion, num_piece = 9)