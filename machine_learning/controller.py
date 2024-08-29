import math
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor# from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import pandas as pd
import torch 
import torch.nn as nn
import torch.optim as optim
from MLPRegressor import MLPRegressor, train_MLPRegressor
from Data import loading_data

datafile1 = 'LimbX_Data.csv'
datafile2 = 'data.csv'

position, angles = loading_data(datafile1, 13, 1)
position2, angles2 = loading_data(datafile2, 7, 1)
X = np.array(position)
Y = np.array(angles)
X_2 = np.array(position2)
Y_2 = np.array(angles2)
positions_total = np.concatenate((X, X_2))
angles_total = np.concatenate((Y, Y_2))

# # THIS IS FOR WHEN THE ANGLES ARE THE INPUT 
# z_scores = np.abs(stats.zscore(angles_total))
# threshold = 2.5
# outlier_indices = np.where(z_scores > threshold)
# # print(z_scores)bb
# positions_total = np.delete(angles_total, outlier_indices, axis=0)
# angles_total = np.delete(positions_total, outlier_indices, axis=0)

# SPLIT INTO, TRAINING, VALIDATION, TEST
pos_train, pos_test, ang_train, ang_test = train_test_split(positions_total, angles_total, test_size=0.15, random_state=42)
pos_train, pos_val, ang_train, ang_val = train_test_split(pos_train, ang_train, test_size=0.15, random_state=42)

# print(pos_train.shape, pos_test.shape)
# print(ang_train.shape, ang_test.shape)

"""

This is for the Machine Learning part of the project. We will be introducing both the Forward Neural Network
and the Inverse Neural Network.

"""

# ----- FORWARD MODEL ------
    
# Prepare the training validation and test data
ang_train = torch.Tensor(ang_train)
pos_train = torch.Tensor(pos_train)
ang_val = torch.Tensor(ang_val)
pos_val = torch.Tensor(pos_val)
ang_test = torch.Tensor(ang_test)
pos_test = torch.Tensor(pos_test)

# TRAINING DATASET
forward_train_data = torch.utils.data.TensorDataset(ang_train, pos_train) # Making a TensorDataset out of the data that we had collected.
forward_train_loader = torch.utils.data.DataLoader(forward_train_data, batch_size=32, shuffle=True)

# VALIDATION DATASET
forward_val_data = torch.utils.data.TensorDataset(ang_val, pos_val)# Making a validation dataset out of the data that we had collected
forward_val_loader = torch.utils.data.DataLoader(forward_val_data, batch_size=32)

# TESTING DATASET
forward_test_data = torch.utils.data.TensorDataset(ang_test, pos_test)
forward_test_loader = torch.utils.data.DataLoader(forward_test_data, batch_size=32)

# Define hyperparameters
forward_input_size = ang_train.shape[1]
forward_output_size = pos_train.shape[1]
forward_hidden_layers = [8, 16, 8, 16]
forward_num_epochs = 4000
forward_learning_rate = 0.01
forward_alpha = 0.2

# CREATING THE FORWARD MODEL 
forward_model = MLPRegressor(forward_input_size, forward_output_size, forward_hidden_layers)

# TRAINING THE FORWARD MODEL
forward_model, forward_train_scores, forward_val_scores = train_MLPRegressor(forward_model, forward_train_loader, forward_val_loader, forward_num_epochs, forward_learning_rate, forward_alpha)


# VALIDATION OF THE FORWARD MODEL
forward_errors = []
forward_model.eval()
# val_loss = 0
print("Validation")
with torch.no_grad():
  # for x, y in forward_val_loader:
  output = forward_model(ang_val) # angles from validation set
  # print(output.shape)
  # forward_pos_pred = forward(output)
  # error = forward_pos_pred - pos_val
  # print(forward_pos_pred)
  # print(pos_val)

  for i in range(len(output)):
      x1, y1 = output[i]
      x2, y2 = pos_val[i] # real pos from validation set
      distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2) 
      print(distance)
      # MEAN SQAURED DISTANCE AS VALIDATION ERROR
      forward_errors.append(distance)

print(f"Average: {sum(forward_errors) / len(forward_errors)}")


# ---------- INVERSE NEURAL NETWORK ------
#### Important note: The input is the position that wants to be reach and the output are the angles. 

# DEFINITION OF FUNCTIONS
# LOSS FUNCTION FOR THE INVERSE NEURAL NETWORK
def nn_loss(ypredicted, Xdesired):
  print(Xdesired.shape, ypredicted.shape)
  loss = torch.mean((Xdesired - ypredicted)**2)
  return loss


def train_inverse(model, train_loader, val_loader, num_epochs, learning_rate, alpha):

  optimizer = optim.Adam(inverse.parameters(), lr=learning_rate, weight_decay=alpha)
  train_scores = []
  val_scores = []
  loss = []

  for epoch in range(num_epochs):
    print("Epoch", epoch)
    inverse.train() # This is setting the mode in which we are in.
    train_loss = 0
    for pos, _ in train_loader:
        optimizer.zero_grad()
        output = inverse(pos) # this gives us a prediction of an angle
        # We want to check whether the prediction of the angle reaches the position that we want, so we pas sit into the forward model
        forward_angle_pred = forward_model(output) # This gives us a prediction for the position based on the angle that we predicted with the inverse model
        # We calculate the loss between the position based on the predicted angle and the actual position given an angle
        loss= nn_loss(forward_angle_pred, pos)
        loss.backward()
        optimizer.step()
        train_loss += loss.item() * pos.shape[0]
        print(train_loss)
    
    train_loss /= len(train_loader.dataset)
    train_scores.append(train_loss)
  
  # Evaluation on the validation set
    # inverse.eval()
    # val_loss = 0
    # print("Validation")
    # with torch.no_grad():
    #   for x, y in val_loader:
    #     output = inverse(x)
    #     forward_angle_pred = forward(output)
    #     loss_val = nn_loss(output, forward_angle_pred)
    #     val_loss += loss_val.item() * x.shape[0]
    #   val_loss /= len(pos_val)
    #   val_scores.append(val_loss)

  val_scores = []
  return model, train_scores, val_scores

  # print(f"Epoch {epoch+1}/{num_epochs}, Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")

# SETTING UP THE INVERSE NM

# Define hyperparameters
input_size = pos_train.shape[1]
output_size = ang_train.shape[1]
hidden_layers = [8, 16, 8]
num_epochs = 5000
learning_rate = 0.01
alpha = 0.5

# Convert data to PyTorch tensors and create data loaders
ang_train = torch.Tensor(ang_train)
pos_train = torch.Tensor(pos_train)
inverse_train_data = torch.utils.data.TensorDataset(pos_train, ang_train) # pos_train and ang_train are switched here from the forward nneural network
inverse_train_loader = torch.utils.data.DataLoader(inverse_train_data, batch_size=32, shuffle=True)

ang_val = torch.Tensor(ang_val)
pos_val = torch.Tensor(pos_val)
ang_test = torch.Tensor(ang_test)
pos_test = torch.Tensor(pos_test)

# DataLOADER
inverse_val_data = torch.utils.data.TensorDataset(pos_val, ang_val)
inverse_val_loader = torch.utils.data.DataLoader(inverse_val_data, batch_size=32)
inverse_test_data = torch.utils.data.TensorDataset(pos_test, ang_test)
inverse_test_loader = torch.utils.data.DataLoader(inverse_test_data, batch_size=32)

# Create and train the model
inverse = MLPRegressor(input_size, output_size, hidden_layers)
inverse, inverse_train_scores, inverse_val_scores = train_inverse(inverse, inverse_train_loader, inverse_val_loader, num_epochs, learning_rate, alpha)

# VALIDATION
errors = []

inverse.eval()
val_loss = 0
print("Validation")
with torch.no_grad():
  # for x, y in val_loader2:
  output = inverse(pos_val)
  print(output.shape)
  forward_pos_pred = forward_model(output)
  # error = forward_pos_pred - pos_val
  # print(forward_pos_pred)
  # print(pos_val)

  for i in range(len(forward_pos_pred)):
      x1, y1 = forward_pos_pred[i]
      x2, y2 = pos_val[i]
      distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
      print(distance)
      errors.append(distance)
  
    # error = math.sqrt((forward_pos_pred[0] - pos_val[0])**2 + (forward_pos_pred[1] - pos_val[1])**2)
    # errors.append(error)

    # loss_val = nn_loss(forward_pos_pred, pos_val)
    # val_loss += loss_val.item() * pos_val.shape[0]
  # val_loss /= len(pos_val)

print(f"Average: {sum(errors) / len(errors)}")


# SAVING/LOADING THE MODEL
torch.save(inverse.state_dict(), 'inverse.pt')
torch.save(forward_model.state_dict(), 'forward_model.pt')

print(f"Input Size: forward = {forward_input_size}, inverse = {input_size}")
print(f"Output Size: forward = {forward_output_size}, inverse = {output_size}")
print(f"Hidden layers: forward = {forward_hidden_layers}, inverse = {hidden_layers}")

# Load the model from a file
my_model = MLPRegressor(input_size, output_size, hidden_layers)  # Create an instance of the model
my_model.load_state_dict(torch.load('inverse.pt'))  # Load the saved parameters into the model