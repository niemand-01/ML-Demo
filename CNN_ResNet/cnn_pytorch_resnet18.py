# -*- coding: utf-8 -*-
"""CNN-Pytorch-ResNet18.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_kDXGSY35qD7DQJqDfn0cYO9OZF9cf8S
"""

import torch
import torch.nn as nn
from torchvision import transforms
import torchvision
import torch.nn.functional as F

# device configuration
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# hyper parameters
Epochs = 20
batch_size = 64
learning_rate =0.001
classes = 10

# image preprocessing modules
transform = transforms.Compose([
                #先padding=4
                transforms.Pad(4),
                #图像一半的概率翻转，一半的概率不翻转
                transforms.RandomHorizontalFlip(),
                #把图像随机裁剪成32*32
                transforms.RandomCrop(32),
                transforms.ToTensor(),])

# cifar10 32*32*3
train_dataset = torchvision.datasets.CIFAR10(root="./cifar10_data",train=True,transform=transform,download=True)
test_dataset = torchvision.datasets.CIFAR10(root="./cifar10_data",train=False,transform=transforms.ToTensor(),download=True)

trainloader = torch.utils.data.DataLoader(dataset=train_dataset,batch_size=batch_size,shuffle=True)
testloader = torch.utils.data.DataLoader(dataset=test_dataset,batch_size=batch_size,shuffle=False)

"""# Single Residual Blcok"""

from IPython.display import Image
Image(url="https://img-blog.csdn.net/2018042621572485?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bnFpYW5kZTg4/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70")

# residualBlock 继承nn.module类
class ResidualBlock(nn.Module):
  def __init__(self,in_channels,out_channels,stride=1):
    super().__init__()
    self.conv_left = nn.Sequential(
        # downsample if stride != 1
        nn.Conv2d(in_channels,out_channels,3,stride,padding=1,bias=False),
        nn.BatchNorm2d(out_channels),
        nn.ReLU(inplace=True),
        # maintain shape
        nn.Conv2d(out_channels,out_channels,3,stride=1,padding=1,bias=False),
        nn.BatchNorm2d(out_channels)
    )

    self.shortcut = nn.Sequential()
    if stride != 1 or in_channels != out_channels:
      self.shortcut = nn.Sequential(
          nn.Conv2d(in_channels,out_channels,3,stride=stride,padding=1,bias=False),
          nn.BatchNorm2d(out_channels)
      )

  def forward(self,input):
    residual = input
    x = self.conv_left(input)
    shortcut = self.shortcut(residual)
    # print(r"left shape:{},right shape:{}".format(x.size(),shortcut.size()))
    # residual shortcut
    x = x + shortcut
    output = F.relu(x)
    return output

"""# ResNet18 Overview
## Remark
1. for each ResidualBlock we have 2 layers and we build 2 Residualblocks, which means 4 layers
2. we downsample only in first ResidualBlock and keep dim in the second Residualblock
3. In the first Residualblock we only downsample at first layer and keep dim at the second layer
4. shortcut is the same as input if we have same dimension at in/-output channels
5. shortcut must also be downsampled if in/-ouput channels are different
"""

Image(url="https://img-blog.csdn.net/20180426215052446?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bnFpYW5kZTg4/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70")

# ResNet
class ResNet(nn.Module):
  def __init__(self,block,layers,num_classes=10):
    super().__init__()
    self.in_channels = 64
    self.prepare_conv = nn.Sequential(
        nn.Conv2d(3,64,3,stride=1,padding=1,bias=False),
        nn.BatchNorm2d(64),
        nn.ReLU(inplace=True),
    )
    self.layer1 = self.make_layer(block,64,blocks_num=2,stride=1)
    self.layer2 = self.make_layer(block,128,blocks_num=2,stride=2)
    self.layer3 = self.make_layer(block,256,blocks_num=2,stride=2)
    self.layer4 = self.make_layer(block,512,blocks_num=2,stride=2) 
    self.fc = nn.Linear(512,num_classes)

  def make_layer(self,block,out_channels,blocks_num=2,stride=1):
    # first block with stride 2(downsample), second block with stride 1 maintaining image dim
    strides = [stride] + [1] * (blocks_num-1) #[2,1] or [1,1]
    layers = []
    for stride in strides:
      layers.append(block(self.in_channels,out_channels,stride))
      self.in_channels = out_channels
    return nn.Sequential(*layers)

  def forward(self,input):
    x = self.prepare_conv(input)

    x = self.layer1(x)
    x = self.layer2(x)
    x = self.layer3(x)
    x = self.layer4(x)

    x = F.avg_pool2d(x,4)
    # tensor.view() is like reshape() with the size -1 is inferred from other dimensions
    # e.g. (4,4) --->view(16,-1) == (16,1) --->view(8,-1) == (8,2)
    # basically it's like x.flatten() == x.view(x.size(0),-1)
    x = x.view(x.size(0),-1)
    x = self.fc(x)
    return x

# define model
model = ResNet(ResidualBlock,[2,2,2,2]).to(device)

"""# model summary"""

from torchsummary import summary

summary(model.cpu(),input_size=(3,32,32))

# loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(),lr=learning_rate)

# updating learning rate
def update_lr(optimizer,lr):
  for param_group in optimizer.param_groups:
    param_group['lr'] = lr 

# train model
per_epoch_total_step = len(trainloader)
current_lr = learning_rate
sum_loss = 0.0
total_label = 0
correct_label = 0
for epoch in range(Epochs):
  for i,(x,y) in enumerate(trainloader):
    x = x.to(device)
    y = y.to(device)
    # optimizer 
    optimizer.zero_grad()

    # forward
    prediction = model(x)
    loss = criterion(prediction,y)

    # backward
    
    loss.backward()
    optimizer.step()

    # print for every batch loss
    sum_loss += loss.item()
    _, predicted = torch.max(prediction.data, 1)
    total_label += y.size(0)
    correct_label += predicted.eq(y.data).cpu().sum()
    print(r'[epoch:{:d}, current_iter:{:d}, total iter:{:d}] Avg Loss: {:.3f} | Acc: {:.3f} '.format(epoch + 1, i, (epoch+1)*per_epoch_total_step, torch.true_divide(sum_loss,(i + 1)), 100. * torch.true_divide(correct_label,total_label)))

    # print for every epoch
    if (i+1)% 100 == 0:
      template = r"Epoch:{}/{},step:{}/{},Loss:{:.6f}"
      print(template.format(epoch+1,Epochs,i+1,per_epoch_total_step,loss.item()))

    # lr decay
    if (epoch+1) % 20 ==0:
      current_lr = current_lr/2
      update_lr(optimizer,current_lr)

