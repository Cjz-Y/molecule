import torch.nn as nn
import torch.nn.functional as F
from .utils import load_state_dict_from_url


model_url = ''


class SimpleModel(nn.Module):
    """
    简单模型
    """

    def __init__(self, input_node):
        super(SimpleModel, self).__init__()
        self.fc1 = nn.Linear(input_node, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, 32)
        self.fc5 = nn.Linear(32, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = self.fc5(x)
        return x


def sample_model(pretrained=False, progress=True, **kwargs):
    """
    从服务器上返回预训练的模型
    :param pretrained: 如果是True，返回预训练的模型
    :param progress: 如果是True，显示加载进度
    :param kwargs:
    :return:
    """

    model = SimpleModel(**kwargs)
    if pretrained:
        state_dict = load_state_dict_from_url(model_url, progress=progress)
        model.load_state_dict(state_dict)
    return model