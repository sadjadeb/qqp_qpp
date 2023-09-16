from sentence_transformers import InputExample, SentenceTransformer, losses
from torch.utils.data import DataLoader
import pickle
import math
import os
import torch

batch_size = 16
epoch_num = 1
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
model_name = 'bert-base-uncased'
model_path = f"output/QPP_bi_{model_name.split('/')[-1]}_matched"

os.makedirs(model_path, exist_ok=True)

model = SentenceTransformer('bert-base-uncased', device=device)

with open('data/pkl_files/train_all-MiniLM-L6-v2_mrr10.pkl', 'rb') as f:
    q_dic_train = pickle.load(f)

train_set = []
for key in q_dic_train:
    q_text = q_dic_train[key]["qtext"]
    first_doc_text = q_dic_train[key]["doc_text"]
    actual_map = q_dic_train[key]["performance"]
    qp_text = q_dic_train[key]["matched_qtext"]
    qp_performance = q_dic_train[key]["matched_performance"]
    # concatenate the query, the query', the performance of query' and the first retrieved document using [SEP] token
    concatenated_text1 = q_text + " [SEP] " + qp_text
    concatenated_text2 = qp_performance + " [SEP] " + first_doc_text
    train_set.append(InputExample(texts=[concatenated_text1, concatenated_text2], label=actual_map))

train_dataloader = DataLoader(train_set, shuffle=True, batch_size=batch_size)
train_loss = losses.CosineSimilarityLoss(model)

# Configure the training
warmup_steps = math.ceil(len(train_dataloader) * epoch_num * 0.1)  # 10% of train data for warm-up

# Train the model
model.fit(train_objectives=[(train_dataloader, train_loss)],
          epochs=epoch_num,
          warmup_steps=warmup_steps,
          output_path=model_path)
model.save(model_path)
print("Model saved to:", model_path)
