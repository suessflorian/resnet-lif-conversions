import os
from torch.utils.data import DataLoader
from torchvision.models.resnet import ImageClassification
from torchvision import datasets, transforms
from typing import Tuple

DATA = os.path.join(os.path.dirname(__file__), "data")


def cifar100(preprocess: ImageClassification, batch_size: int) -> Tuple[DataLoader, DataLoader]:
    test_transforms = transforms.Compose([preprocess])
    train_dataset = datasets.CIFAR100(root=DATA, train=True, download=True, transform=test_transforms)
    test_dataset = datasets.CIFAR100(root=DATA, train=False, download=True, transform=preprocess)

    train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader
