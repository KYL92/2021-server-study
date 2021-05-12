import torch.nn as nn


class FER_CNN(nn.Module):
    def __init__(self):
        super(FER_CNN, self).__init__()
        self.cnn1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3)
        self.cnn2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3)
        self.cnn3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3)
        self.cnn4 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3)
        self.cnn5 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3)
        self.cnn6 = nn.Conv2d(in_channels=256, out_channels=128, kernel_size=3)
        self.cnn7 = nn.Conv2d(in_channels=128, out_channels=64, kernel_size=3)
        self.relu = nn.ReLU()
        self.pool1 = nn.MaxPool2d(2, 1)
        self.pool2 = nn.MaxPool2d(2, 2)
        self.cnn1_bn = nn.BatchNorm2d(16)
        self.cnn2_bn = nn.BatchNorm2d(32)
        self.cnn3_bn = nn.BatchNorm2d(64)
        self.cnn4_bn = nn.BatchNorm2d(128)
        self.cnn5_bn = nn.BatchNorm2d(256)
        self.cnn6_bn = nn.BatchNorm2d(128)
        self.cnn7_bn = nn.BatchNorm2d(64)
        self.fc1 = nn.Linear(256, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 7)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = self.relu(self.pool1(self.cnn1_bn(self.cnn1(x))))
        x = self.relu(self.pool1(self.cnn2_bn(self.dropout(self.cnn2(x)))))
        x = self.relu(self.pool1(self.cnn3_bn(self.cnn3(x))))
        x = self.relu(self.pool1(self.cnn4_bn(self.dropout(self.cnn4(x)))))
        x = self.relu(self.pool2(self.cnn5_bn(self.cnn5(x))))
        x = self.relu(self.pool2(self.cnn6_bn(self.dropout(self.cnn6(x)))))
        x = self.relu(self.pool2(self.cnn7_bn(self.dropout(self.cnn7(x)))))

        x = x.view(x.size(0), -1)

        x = self.relu(self.dropout(self.fc1(x)))
        x = self.relu(self.dropout(self.fc2(x)))
        x = self.fc3(x)
        return x

    def count_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)