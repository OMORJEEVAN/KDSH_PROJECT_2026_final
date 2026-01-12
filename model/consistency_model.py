import torch.nn as nn

class ConsistencyModel(nn.Module):
    def __init__(self, input_dim=384):
        super().__init__()
        self.classifier = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 1)
        )

    def forward(self, x):
        return self.classifier(x)