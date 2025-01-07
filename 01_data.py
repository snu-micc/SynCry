import glob
import json
import random
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split



dir = "./data/cifstrings_mp30/" # path to the directory containing the json files of cifstrings
mp_list = glob.glob(dir+"m*.json")

data = []
for mp_dir in tqdm(mp_list):
    with open(mp_dir, "r") as jsonfile:
        d = json.load(jsonfile)
        data.append(d)


print(d.keys()) # dict_keys(['material_id', 'formula', 'icsd', 'cifstrings'])


p_count = 0
p_data = []
u_count = 0
u_data = []
for d in data:
    if d['icsd'] == False:
        u_count += 1
        u_data.append(d)
    elif d['icsd'] == True:
        p_count += 1
        p_data.append(d)

print(p_count/u_count)


train_p, hold_out_p = train_test_split(p_data, test_size=0.2, random_state=7)
train_p, val_p = train_test_split(train_p, test_size=0.2, random_state=7)
train_u, hold_out_u = train_test_split(u_data, test_size=0.2, random_state=7)
train_u, val_u = train_test_split(train_u, test_size=0.2, random_state=7)

random.shuffle(train_p)
random.shuffle(val_p)
random.shuffle(hold_out_p)
random.shuffle(train_u)
random.shuffle(val_u)
random.shuffle(hold_out_u)

train_data = []
val_data = []
hold_out_data = []
for i, d in enumerate(train_p):
    request = {}
    request["messages"] = [
        {"role":"user", "content": "You are an expert inorganic chemist.  Determine if the following compound is likely to be synthesizable based on its structural description, answering only \"P\" (for positive or possible) and \"U\" (for unknown or unlikely): "+ d["description"]},
        {"role":"assistant", "content": "P"}
    ]
    train_data.append(request)


for i, d in enumerate(train_u):
    request = {}
    request["messages"] = [
        {"role":"user", "content": "You are an expert inorganic chemist.  Determine if the following compound is likely to be synthesizable based on its structural description, answering only \"P\" (for positive or possible) and \"U\" (for unknown or unlikely): "+ d["description"]},
        {"role":"assistant", "content": "U"}
    ]
    train_data.append(request)
    if i == len(train_p) -1:
        break


for i, d in enumerate(val_p):
    request = {}
    request["messages"] = [
        {"role":"user", "content": "You are an expert inorganic chemist.  Determine if the following compound is likely to be synthesizable based on its structural description, answering only \"P\" (for positive or possible) and \"U\" (for unknown or unlikely): "+ d["description"]},
        {"role":"assistant", "content": "P"}
    ]
    val_data.append(request)


for i, d in enumerate(val_u):
    request = {}
    request["messages"] = [
        {"role":"user", "content": "You are an expert inorganic chemist.  Determine if the following compound is likely to be synthesizable based on its structural description, answering only \"P\" (for positive or possible) and \"U\" (for unknown or unlikely): "+ d["description"]},
        {"role":"assistant", "content": "U"}
    ]
    val_data.append(request)
    if i == len(val_p) -1:
        break


for i, d in enumerate(hold_out_p):
    request = {}
    request["messages"] = [
        {"role":"user", "content": "You are an expert inorganic chemist.  Determine if the following compound is likely to be synthesizable based on its structural description, answering only \"P\" (for positive or possible) and \"U\" (for unknown or unlikely): "+ d["description"]},
        {"role":"assistant", "content": "P"}
    ]
    hold_out_data.append(request)


for i, d in enumerate(hold_out_u):
    request = {}
    request["messages"] = [
        {"role":"user", "content": "You are an expert inorganic chemist.  Determine if the following compound is likely to be synthesizable based on its structural description, answering only \"P\" (for positive or possible) and \"U\" (for unknown or unlikely): "+ d["description"]},
        {"role":"assistant", "content": "U"}
    ]
    hold_out_data.append(request)


print(len(train_data), len(val_data), len(hold_out_data))


random.shuffle(train_data)
random.shuffle(val_data)
random.shuffle(hold_out_data)

save_dir = "./data/finetuning"
with open(save_dir+"/train_pu_struct_data.jsonl" , encoding= "utf-8",mode="w") as file:
    for i in train_data:
        file.write(json.dumps(i) + "\n")
with open(save_dir+"/val_pu_struct_data.jsonl" , encoding= "utf-8",mode="w") as file:
    for i in val_data:
        file.write(json.dumps(i) + "\n")
with open(save_dir+"/hold_out_pu_struct_data.jsonl" , encoding= "utf-8",mode="w") as file:
    for i in hold_out_data:
        file.write(json.dumps(i) + "\n")
        