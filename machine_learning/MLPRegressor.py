import torch
import torch.nn as nn
import torch.optim as optim


#Define the MLP model
class MLPRegressor(nn.Module):
    def __init__(self, input_size, output_size, hidden_layers):
        super(MLPRegressor, self).__init__()
        layers = []
        prev_layer_size = input_size
        for layer_size in hidden_layers:
            layers.append(nn.Linear(prev_layer_size, layer_size))
            layers.append(nn.ReLU())
            prev_layer_size = layer_size
        layers.append(nn.Linear(prev_layer_size, output_size))
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)

    def compute_gradient(self, x, i):
        x.requires_grad = True
        output = self.forward(x)
        gradient = torch.autograd.grad(output[0][i], x, retain_graph=True)[0][0]
        return gradient.detach().numpy()
    
# Define the training function
def train_MLPRegressor(model, train_loader, val_loader, num_epochs, learning_rate, alpha):
    optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=alpha)
    criterion = nn.MSELoss()

    train_scores = []
    val_scores = []
    loss = []

    for epoch in range(num_epochs):
        model.train()
        train_loss = 0
        for x, y in train_loader:
            optimizer.zero_grad()
            output = model(x)
            batch_loss = criterion(output, y)
            batch_loss.backward()
            optimizer.step()
            train_loss += batch_loss.item() * x.shape[0]
        train_loss /= len(train_loader.dataset)
        train_scores.append(train_loss)

        model.eval()
        val_loss = 0
        with torch.no_grad():
            for x, y in val_loader:
                output = model(x)
                batch_loss = criterion(output, y)
                val_loss += batch_loss.item() * x.shape[0]
            val_loss /= len(val_loader.dataset)
            val_scores.append(val_loss)
    # val_scores = []
        print(f"Epoch {epoch+1}/{num_epochs}, Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
    
    return model, train_scores, val_scores
