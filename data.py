import os
from torch.utils.data import DataLoader
from torchvision.models.resnet import ImageClassification
from torchvision import datasets, transforms
from torchvision.transforms import v2
from typing import Tuple

DATA = os.path.join(os.path.dirname(__file__), "data")

def cifar100(preprocess: ImageClassification, batch_size: int, device: str = "mps") -> Tuple[DataLoader, DataLoader]:
    num_workers = 1
    if device == "cuda":
        num_workers = 2

    train_transforms = transforms.Compose([
        preprocess,
        v2.RandomHorizontalFlip(),
        v2.RandomVerticalFlip(),
        v2.RandomRotation(degrees=(-15, 15)),
        v2.RandomResizedCrop(size=(224, 224), scale=(0.8, 1.0)),
        v2.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        v2.RandomGrayscale(p=0.1),
        v2.RandomPerspective(distortion_scale=0.5, p=0.5),
        v2.GaussianBlur(kernel_size=(5, 9), sigma=(0.1, 5)),
    ])

    train_dataset = datasets.CIFAR100(root=DATA, train=True, download=True, transform=train_transforms)
    test_dataset = datasets.CIFAR100(root=DATA, train=False, download=True, transform=preprocess)


    if device == "cuda":
        train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers, pin_memory=True, pin_memory_device=device)
        test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=True, pin_memory_device=device)
    else:
        train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
        test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)

    return train_loader, test_loader

def cifar10(preprocess: ImageClassification, batch_size: int, device: str = "mps") -> Tuple[DataLoader, DataLoader]:
    test_transforms = transforms.Compose([preprocess])
    train_dataset = datasets.CIFAR10(root=DATA, train=True, download=True, transform=test_transforms)
    test_dataset = datasets.CIFAR10(root=DATA, train=False, download=True, transform=preprocess)

    train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader

def fashionMNIST(preprocess: ImageClassification, batch_size: int, device: str = "mps") -> Tuple[DataLoader, DataLoader]:
    test_transforms = transforms.Compose([transforms.Grayscale(num_output_channels=3), preprocess])
    train_transforms = transforms.Compose([transforms.Grayscale(num_output_channels=3), preprocess])

    train_dataset = datasets.FashionMNIST(root=DATA, train=True, download=True, transform=test_transforms)
    test_dataset = datasets.FashionMNIST(root=DATA, train=False, download=True, transform=train_transforms)

    train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader


LOADER = {
    "cifar100": cifar100,
    "cifar10": cifar10,
    "fashionMNIST": fashionMNIST,
}

def loader(dataset: str, preprocess: ImageClassification, batch_size: int, device: str = "mps") -> Tuple[DataLoader, DataLoader]:
    return LOADER[dataset](preprocess, batch_size, device)

