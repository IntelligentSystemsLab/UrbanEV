import os

import torch
import torch.nn as nn
import numpy as np
from torch_geometric_temporal.nn.attention.astgcn import ASTGCN
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
import warnings
class Lo:
    def __init__(self, args):
        self.args = args
        self.pred_len = args.pre_len

    def predict(self, train_valid_occ, test_occ):
        """
        Use the latest observed value as the prediction for the next time step.
        """
        time_len, node = test_occ.shape
        preds = np.zeros((time_len, node))

        for j in range(node):
            for i in range(time_len):
                if i < self.pred_len:
                    preds[i, j] = train_valid_occ[-self.pred_len + i, j]
                else:
                    preds[i, j] = test_occ[i - self.pred_len, j]

        return preds


class Ar:
    def __init__(self, pred_len, args, lags=1):
        """
        Initialize the AR model parameters.

        Args:
            lags (int): The number of lagged observations to use in the model.
        """
        self.args = args
        self.pred_len = pred_len
        self.lags = lags

    def predict(self, train_valid_occ, test_occ):
        """
        Perform predictions using the AR model.
        """
        time_len, node = test_occ.shape
        train_valid_occ = train_valid_occ[:-self.pred_len, :]
        preds = np.zeros((time_len, node))

        for j in range(node):  # Train and predict for each node
            fit_series = train_valid_occ[:, j]

            # Train AR model on each node
            model = AutoReg(fit_series, lags=self.lags)
            model_fitted = model.fit()
            for i in range(time_len):
                start = len(fit_series) + self.pred_len
                end = start
                pred = model_fitted.predict(start=start, end=end)
                preds[i, j] = pred[0]  # Ensure single value is assigned

        return preds

class Arima:
    def __init__(self, pred_len, args, p=1, d=1, q=1):
        """
        Initialize the ARIMA model parameters.
        """
        self.pred_len = pred_len
        self.args = args
        self.p = p
        self.d = d
        self.q = q

    def predict(self, train_valid_occ, test_occ):
        time_len, node = test_occ.shape
        train_valid_occ = train_valid_occ[:-self.pred_len, :]
        preds = np.zeros((time_len, node))
        warnings.filterwarnings("ignore", category=UserWarning,
                                message=".*Maximum Likelihood optimization failed to converge.*")
        for j in range(node):  # Train and predict for each node
            fit_series = train_valid_occ[:, j]

            # Train ARIMA model on each node
            model = ARIMA(fit_series, order=(self.p, self.d, self.q))
            model_fitted = model.fit()

            # Predict using the ARIMA model
            for i in range(time_len):
                start = len(fit_series) + self.pred_len
                end = start
                pred = model_fitted.predict(start=start, end=end)
                preds[i, j] = pred[0]  # Ensure single value is assigned

        return preds


class Fcnn(nn.Module):
    def __init__(self,n_fea, node=247, seq=12):  # input_dim = seq_length
        super(Fcnn, self).__init__()
        self.num_feat = n_fea
        self.seq = seq
        self.nodes = node
        self.linear = nn.Linear(seq*n_fea, 1)

    def forward(self, occ,extra_feat='None'):
        x = occ # batch, nodes,seq for region or batch, seq for nodes
        if extra_feat != 'None':
            x = torch.cat([occ.unsqueeze(-1), extra_feat], dim=-1)
            assert x.shape[-1] == self.num_feat, f"Number of features ({x.shape[-1]}) does not match n_fea ({self.num_feat})."
        x = x.view(-1,self.nodes,self.seq *self.num_feat)
        x = self.linear(x)
        x = torch.squeeze(x)
        return x


class Lstm(nn.Module):
    def __init__(self, seq, n_fea, node=331):
        super(Lstm, self).__init__()
        self.num_feat = n_fea
        self.nodes = node
        self.seq_len = seq
        self.encoder = nn.Linear(n_fea,1)# input.shape: [batch, channel, width, height]
        self.lstm_hidden_dim = 16
        self.lstm = nn.LSTM(input_size=n_fea, hidden_size=self.lstm_hidden_dim, num_layers=2,
                            batch_first=True)
        self.linear = nn.Linear(seq * self.lstm_hidden_dim, 1)

    def forward(self, occ, extra_feat=None):  # occ.shape = [batch, node, seq]
        x = occ.unsqueeze(-1)
        if extra_feat != 'None':
            x = torch.cat([occ.unsqueeze(-1), extra_feat], dim=-1)
        assert x.shape[-1] == self.num_feat, f"Number of features ({x.shape[-1]}) does not match n_fea ({self.num_feat})."

        bs = x.shape[0]
        x = x.view(bs * self.nodes, self.seq_len, self.num_feat)

        lstm_out, _ = self.lstm(x)  # lstm_out shape: [batch_size * node, seq_len, lstm_hidden_dim]
        lstm_out = lstm_out.reshape(bs, self.nodes, self.seq_len * self.lstm_hidden_dim)
        x = self.linear(lstm_out)
        x = torch.squeeze(x)
        return x


class Gcn(nn.Module):
    def __init__(self, seq, n_fea, adj_dense, gcn_hidden=32, gcn_layers=2):
        super(Gcn, self).__init__()
        self.nodes = adj_dense.shape[0]
        self.gcn_hidden = gcn_hidden
        self.gcn_layers = gcn_layers
        self.num_feat = n_fea
        self.act = nn.ReLU()
        self.encoder = nn.Conv2d(self.nodes, self.nodes, (1, n_fea))

        # Calculate A_delta matrix (normalized adjacency)
        deg = torch.sum(adj_dense, dim=0)
        deg = torch.diag(deg)
        deg_delta = torch.linalg.inv(torch.sqrt(deg))
        a_delta = torch.matmul(torch.matmul(deg_delta, adj_dense), deg_delta)
        self.A = a_delta

        # Define GCN layers
        self.gcn_layers_list = nn.ModuleList()
        self.gcn_layers_list.append(nn.Linear(seq, self.gcn_hidden))  # Input to first GCN layer
        for _ in range(self.gcn_layers - 1):
            self.gcn_layers_list.append(nn.Linear(self.gcn_hidden, self.gcn_hidden))

        self.decoder = nn.Linear(self.gcn_hidden+seq, 1)

    def forward(self, occ, extra_feat=None):
        x = occ.clone().unsqueeze(-1)  # Add feature dimension
        if extra_feat != 'None':
            x = torch.cat([occ.unsqueeze(-1), extra_feat], dim=-1)
        assert x.shape[-1] == self.num_feat, f"Number of features ({x.shape[-1]}) does not match n_fea ({self.num_feat})."

        # GCN forward pass
        x = self.encoder(x)
        batch_size, node, seq_len = occ.size()
        gcn_out = x.view(batch_size, node, -1)  # Flatten sequence and features into [batch, node, seq * n_fea]

        for gcn_layer in self.gcn_layers_list:
            gcn_out = gcn_layer(gcn_out)
            gcn_out = torch.matmul(self.A, gcn_out)
            gcn_out = self.act(gcn_out)

        combined_out = torch.cat((occ, gcn_out), dim=-1)
        x = self.decoder(combined_out)
        x = torch.squeeze(x)

        return x


class Gcnlstm(nn.Module):
    def __init__(self, seq, n_fea, adj_dense, node=307, gcn_out=32, gcn_layers=1, lstm_hidden_dim=256, lstm_layers=2,
                 hidden_dim=32):
        super(Gcnlstm, self).__init__()

        self.nodes = node
        self.seq_len = seq
        self.num_feat = n_fea
        self.lstm_hidden_dim = lstm_hidden_dim
        self.lstm_layers = lstm_layers
        self.gcn_out = gcn_out
        self.gcn_layers = gcn_layers
        self.hidden_dim = hidden_dim

        # Initialize GCN layers
        self.gcn_layers_list = nn.ModuleList()
        for i in range(gcn_layers):
            in_dim = seq * n_fea if i == 0 else gcn_out
            self.gcn_layers_list.append(nn.Linear(in_dim, gcn_out))
        self.act = nn.ReLU()

        self.encoder = nn.Conv2d(self.nodes, self.nodes, (1, n_fea))
        # Initialize LSTM layer
        self.lstm = nn.LSTM(input_size=n_fea, hidden_size=self.lstm_hidden_dim, num_layers=self.lstm_layers,
                            batch_first=True)
        self.decoder = nn.Linear(seq + self.gcn_out + self.lstm_hidden_dim, 1)
        # Calculate A_delta matrix
        deg = torch.sum(adj_dense, dim=0)
        deg = torch.diag(deg)
        deg_delta = torch.linalg.inv(torch.sqrt(deg))
        a_delta = torch.matmul(torch.matmul(deg_delta, adj_dense), deg_delta)
        self.A = a_delta

    def forward(self, occ, extra_feat=None):
        x = occ.clone().unsqueeze(-1)  # Add feature dimension
        if extra_feat != 'None':
            x = torch.cat([occ.unsqueeze(-1), extra_feat], dim=-1)
        assert x.shape[-1] == self.num_feat, f"Number of features ({x.shape[-1]}) does not match n_fea ({self.num_feat})."
        # Create a copy of occ to avoid modifying the original data
        x = self.encoder(x)
        x_copy = x.clone().unsqueeze(-1)
        batch_size = x_copy.size(0)

        # Process all timesteps with LSTM
        x_lstm = x_copy.view(batch_size * self.nodes, self.seq_len, self.num_feat)
        lstm_out, _ = self.lstm(x_lstm)
        lstm_out = lstm_out.view(batch_size, self.nodes, self.seq_len,
                                 self.lstm_hidden_dim)  # Shape: (batch, node, seq, lstm_hidden_dim)

        # Process with GCN layers
        gcn_out = x.view(batch_size,self.nodes,self.seq_len * self.num_feat)
        for gcn_layer in self.gcn_layers_list:
            gcn_out = gcn_layer(gcn_out)
            gcn_out = torch.matmul(self.A, gcn_out)
            gcn_out = self.act(gcn_out)

        # Concatenate LSTM and GCN outputs
        combined_out = torch.cat((occ,lstm_out[:,:,-1,:], gcn_out), dim=-1)  # Shape: (batch, node, seq, lstm_hidden_dim + gcn_out)

        x = self.decoder(combined_out)
        x = torch.squeeze(x)
        return x


class Astgcn(ASTGCN):
    def __init__(self, adj_dense,nb_block,in_channels, K, nb_chev_filter, nb_time_filter, time_strides, num_for_predict,len_input,num_of_vertices,node_idx=None):
        super(Astgcn, self).__init__(nb_block,in_channels, K, nb_chev_filter, nb_time_filter, time_strides, num_for_predict,len_input,num_of_vertices,normalization=None)
        
        # self.fc = nn.Linear(self.num_nodes, 1)
        # Preprocess the adjacency matrix to create edge_index and edge_weight
        self.node_idx = node_idx
        self.adj_dense = adj_dense
        self.num_feat = in_channels
        if self.node_idx is not None:
            filtered_adj = torch.zeros_like(adj_dense)
            filtered_adj[node_idx, :] = adj_dense[node_idx, :]
            filtered_adj[:, node_idx] = adj_dense[:, node_idx]
            self.adj_dense = filtered_adj
        self.edge_index = self.create_edge_index(adj_dense)
        self.edge_weight = adj_dense[adj_dense > 0]

    def create_edge_index(self, adj_dense):
        # Convert dense adjacency matrix to sparse edge index format
        edge_index = torch.nonzero(adj_dense, as_tuple=False).t().contiguous()
        return edge_index

    def forward(self, occ,extra_feat=None):
        x = occ.unsqueeze(-1)  # Add feature dimension
        if extra_feat != 'None':
            x = torch.cat([occ.unsqueeze(-1), extra_feat], dim=-1)
        assert x.shape[-1] == self.num_feat, f"Number of features ({x.shape[-1]}) does not match n_fea ({self.num_feat})."

        x = super().forward(x.transpose(2,3),self.edge_index)
        return x.squeeze(-1)
