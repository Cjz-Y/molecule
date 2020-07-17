from .molecule import MoleculeDataset


class ASEDataset(MoleculeDataset):
    """
    通过对ASE DB解析生成Dataset
    """

    def __init__(self, db):
        super().__init__()

    def __len__(self):
        pass

    def __getitem__(self, item):
        pass
