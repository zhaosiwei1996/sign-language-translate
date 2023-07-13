from torch import nn
from torchinfo import summary
import torch.nn.functional as F


class AutoEncoder(nn.Module):
    def __init__(self, dof):
        super().__init__()
        # dof特征数 63个字段 #256 根据数据大小      15卷积核 63/9个一卷=7
        self.encoder = nn.Sequential(nn.Conv1d(dof, 256, 15, padding=7, padding_mode='replicate'),
                                     # 激活函数？
                                     nn.ReLU(),
                                     nn.MaxPool1d(2),
                                     nn.Dropout(0.2),

                                     # 256个
                                     nn.Conv1d(256, 128, 15, padding=7, padding_mode='replicate'),
                                     nn.ReLU(),
                                     nn.MaxPool1d(2),
                                     nn.Dropout(0.2),

                                     # nn.Conv1d(10, 2, 15, padding=7, padding_mode='replicate'),
                                     # # nn.MaxPool1d(2),
                                     # nn.Tanh()

                                     )
        # 128 * 7, 128 全连接层 128*3
        self.MLP = nn.Sequential(nn.Linear(128 * 7, 128),
                                 nn.ReLU(),
                                 nn.Dropout(0.2),

                                 nn.Linear(128, 32),
                                 nn.ReLU(),
                                 nn.Dropout(0.2),

                                 #填标签数
                                 nn.Linear(32, 20),
                                 nn.ReLU(),
                                 nn.Dropout(0.2),

                                 )

    def forward(self, x):
        x = self.encoder(x)
        x = x.view(-1, 128 * 3)
        x = self.MLP(x)
        return F.log_softmax(x, dim=1)


encoder = AutoEncoder(54)
batch_size = 64
                                 #多少个一组   #特征 #25个一组
summary(model=encoder, input_size=(batch_size, 54, 25))
