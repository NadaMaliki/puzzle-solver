import torch  # type: ignore
import torchvision # type: ignore
import math
import copy
from torch import nn  # type: ignore
from transformer import *
from utils import perfect_sqr

class JigSolver (nn.Module):
    """
    Takes a jumbled image and produces the correct piece location 
    """

    def __init__(self, num_piece = 9, modelname = "resnet", pretrained = False, 
            t_layers = 1, t_multihead = 8, t_dropout = .1, t_ff = 2048):
        super(JigSolver, self).__init__()
        """
        modelname = `resnet` or `vgg`
        """
        assert(perfect_sqr(num_piece), "make sure the num_piece is a perfect square")
        
        self.num_piece = num_piece
        self.sqrt = int(math.sqrt(num_piece))
        if modelname == "vgg":
            self.cnn = torchvision.models.vgg16_bn(pretrained=pretrained)
        else: 
            self.cnn = torchvision.models.resnet34(pretrained=pretrained)

        self.cnn.avgpool = nn.AdaptiveAvgPool2d(output_size=(self.sqrt, self.sqrt))
        modules = list(self.cnn.children())[:-1]
        self.cnn = nn.Sequential(*modules)

        self.position = PositionalEncoding(512, t_dropout, 9)
        attn = MultiHeadedAttention(t_multihead, 512)
        ff = PositionwiseFeedForward(512, t_ff, t_dropout)
        self.transformer = Encoder(EncoderLayer(512, copy.deepcopy(attn), copy.deepcopy(ff), t_dropout), t_layers)

        
        self.linear_list = nn.ModuleList()

        for i in range(num_piece):
            self.linear_list.append(nn.Linear(512, num_piece))


    def forward(self, x):
        m = x.size(0)
        x = self.cnn(x)
        x = x.view(m, -1, 512)
        x = self.position(x)
        x = self.transformer(x)
        x_arr = []
        for i in range(self.num_piece):
            x_arr.append(self.linear_list[i](x[:, i, :]))

        return x_arr


