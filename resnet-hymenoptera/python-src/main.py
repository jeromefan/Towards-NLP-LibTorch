import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as tud
from torchvision import datasets, transforms
from loadData import ImageFolderDataset

if __name__ == "__main__":
    print('Deep Residual Network for Imagefolder Dataset!')

    # Device
    cuda_available = torch.cuda.is_available()
    device = torch.device("cuda" if cuda_available else "cpu")
    print('CUDA available. Training on GPU.') if cuda_available else print(
        'Training on CPU.')

    # Hyper Parameters
    num_classes = 2
    batch_size = 64
    num_epochs = 20
    learning_rate = 1e-3
    MNIST_data_path = '/home/jerome/data/hymenoptera_data'

    # MNIST Dataset
    train_dataset = datasets.MNIST(MNIST_data_path,
                                   train=True,
                                   download=False,
                                   transform=transforms.Compose([transforms.ToTensor(),
                                                                transforms.Normalize(
                                       mean=(0.1307,), std=(0.3081,))])
                                   )
    val_dataset = datasets.MNIST(MNIST_data_path,
                                 train=False,
                                 download=False,
                                 transform=transforms.Compose([transforms.ToTensor(),
                                                               transforms.Normalize(
                                     mean=(0.1307,), std=(0.3081,))])
                                 )

    # Number of samples in the dataset
    num_train_samples = len(train_dataset)
    num_val_samples = len(val_dataset)

    # Data Loaders
    train_loader = tud.DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = tud.DataLoader(val_dataset, batch_size=batch_size)

    print('Data Loaded!')

    # Model
    model = FCnet(input_size, hidden_size, num_classes)
    model.to(device)

    print('Model Created!')

    # Optimizer
    optimizer = optim.SGD(model.parameters(), learning_rate)
    loss_fn = nn.CrossEntropyLoss()

    print('Start Training...')
    for epoch in range(num_epochs):
        # Initialize
        running_loss = 0.0
        for i, (data, target) in enumerate(train_loader):
            batch_num = data.size(0)
            data, target = data.view(
                batch_num, -1).to(device), target.to(device)

            # Forward Pass
            output = model(data)
            loss = loss_fn(output, target)

            # Update running loss
            running_loss += loss.item() * batch_num

            # Backward and Optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        sample_mean_loss = running_loss / num_train_samples
        print(
            f'Epoch [{epoch + 1}/{num_epochs}]  Training Loss: {sample_mean_loss}')

    print('Start Validation...')
    model.eval()
    num_correct = 0
    for i, (data, target) in enumerate(val_loader):
        batch_num = data.size(0)
        data, target = data.view(batch_num, -1).to(device), target.to(device)
        output = model(data)
        prediction = output.argmax(dim=1)
        num_correct += torch.sum(prediction.eq(target))
    val_accuracy = num_correct / num_val_samples
    print(f'Validation Accuracy: {val_accuracy}')
