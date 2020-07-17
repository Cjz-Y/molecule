from torch.utils import data

class MoleculeDataset(data.Dataset):
    """
    所有分子数据集的父类，可以提取一些常规操作放在init方法中
    """

    def __init__(self):
        pass

    def __getitem__(self, index):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError