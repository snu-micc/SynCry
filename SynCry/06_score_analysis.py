import json
import jsonlines
import pandas as pd
import matplotlib.pyplot as plt
import math
from tqdm import tqdm
import glob
import seaborn as sns


u_scores_original = {}
with jsonlines.open("./hold_out_u_score+struct(originaldata).jsonl") as f:
    for i, line in enumerate(f.iter()):
        u_scores_original[f"request-{i}"] = line["u_score"]

with open('./results_prediction_formatted/atom_SynCry-GPT.json', 'r') as jsonfile:
    atom_syncry_gpt = json.load(jsonfile)
with open('./results_prediction_formatted/atom_GPT.json', 'r') as jsonfile:
    atom_gpt = json.load(jsonfile)
with open('./results_prediction_formatted/atom_thermo_SynCry-GPT.json', 'r') as jsonfile:
    atom_thermo_syncry_gpt = json.load(jsonfile)
with open('./results_prediction_formatted/atom_thermo_GPT.json', 'r') as jsonfile:
    atom_thermo_gpt = json.load(jsonfile)
with open('./results_prediction_formatted/free_SynCry-GPT.json', 'r') as jsonfile:
    free_syncry_gpt = json.load(jsonfile)
with open('./results_prediction_formatted/free_GPT.json', 'r') as jsonfile:
    free_gpt = json.load(jsonfile)
with open('./results_prediction_formatted/free_thermo_SynCry-GPT.json', 'r') as jsonfile:
    free_thermo_syncry_gpt = json.load(jsonfile)
with open('./results_prediction_formatted/free_thermo_GPT.json', 'r') as jsonfile:
    free_thermo_gpt = json.load(jsonfile)

atom_syncry_gpt_list = {}
atom_gpt_list = {}
atom_thermo_syncry_gpt_list = {}
atom_thermo_gpt_list = {}
free_syncry_gpt_list = {}
free_gpt_list = {}
free_thermo_syncry_gpt_list = {}
free_thermo_gpt_list = {}
error_count = 0

if 'gpt' in atom_syncry_gpt[0]['Model']:
    for i, pred in enumerate(atom_syncry_gpt):
        try:
            p_check = "U"
            if pred["Prediction1"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs1"])
                p_check = "P"
            elif pred["Prediction2"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs2"])
            elif pred["Prediction3"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs3"])
            atom_syncry_gpt_list[f"{pred['custom_id']}"] = p_score
        except:
            error_count += 1
            atom_syncry_gpt_list[f"{pred['custom_id']}"] = [0]

if 'gpt' in atom_gpt[0]['Model']:
    for i, pred in enumerate(atom_gpt):
        try:
            p_check = "U"
            if pred["Prediction1"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs1"])
                p_check = "P"
            elif pred["Prediction2"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs2"])
            elif pred["Prediction3"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs3"])
            atom_gpt_list[f"{pred['custom_id']}"] = p_score
        except:
            error_count += 1
            atom_gpt_list[f"{pred['custom_id']}"] = [0]

if 'gpt' in atom_thermo_syncry_gpt[0]['Model']:
    for i, pred in enumerate(atom_thermo_syncry_gpt):
        try:
            p_check = "U"
            if pred["Prediction1"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs1"])
                p_check = "P"
            elif pred["Prediction2"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs2"])
            elif pred["Prediction3"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs3"])
            atom_thermo_syncry_gpt_list[f"{pred['custom_id']}"] = p_score
        except:
            error_count += 1
            atom_thermo_syncry_gpt_list[f"{pred['custom_id']}"] = [0]

if 'gpt' in atom_thermo_gpt[0]['Model']:
    for i, pred in enumerate(atom_thermo_gpt):
        try:
            p_check = "U"
            if pred["Prediction1"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs1"])
                p_check = "P"
            elif pred["Prediction2"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs2"])
            elif pred["Prediction3"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs3"])
            atom_thermo_gpt_list[f"{pred['custom_id']}"] = p_score
        except:
            error_count += 1
            atom_thermo_gpt_list[f"{pred['custom_id']}"] = [0]

if 'gpt' in free_syncry_gpt[0]['Model']:
    for i, pred in enumerate(free_syncry_gpt):
        try:
            p_check = "U"
            if pred["Prediction1"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs1"])
                p_check = "P"
            elif pred["Prediction2"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs2"])
            elif pred["Prediction3"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs3"])
            free_syncry_gpt_list[f"{pred['custom_id']}"] = p_score
        except:
            error_count += 1
            free_syncry_gpt_list[f"{pred['custom_id']}"] = [0]

if 'gpt' in free_gpt[0]['Model']:
    for i, pred in enumerate(free_gpt):
        try:
            p_check = "U"
            if pred["Prediction1"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs1"])
                p_check = "P"
            elif pred["Prediction2"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs2"])
            elif pred["Prediction3"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs3"])
            free_gpt_list[f"{pred['custom_id']}"] = p_score
        except:
            error_count += 1
            free_gpt_list[f"{pred['custom_id']}"] = [0]

if 'gpt' in free_thermo_syncry_gpt[0]['Model']:
    for i, pred in enumerate(free_thermo_syncry_gpt):
        try:
            p_check = "U"
            if pred["Prediction1"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs1"])
                p_check = "P"
            elif pred["Prediction2"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs2"])
            elif pred["Prediction3"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs3"])
            free_thermo_syncry_gpt_list[f"{pred['custom_id']}"] = p_score
        except:
            error_count += 1
            free_thermo_syncry_gpt_list[f"{pred['custom_id']}"] = [0]

if 'gpt' in free_thermo_gpt[0]['Model']:
    for i, pred in enumerate(free_thermo_gpt):
        try:
            p_check = "U"
            if pred["Prediction1"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs1"])
                p_check = "P"
            elif pred["Prediction2"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs2"])
            elif pred["Prediction3"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs3"])
            free_thermo_gpt_list[f"{pred['custom_id']}"] = p_score
        except:
            error_count += 1
            free_thermo_gpt_list[f"{pred['custom_id']}"] = [0]

print("Error count:", error_count)

integrated_dic = {}

for key in u_scores_original.keys():
    integrated_dic[key] = [u_scores_original.get(key), atom_syncry_gpt_list.get(key), atom_gpt_list.get(key), atom_thermo_syncry_gpt_list.get(key), atom_thermo_gpt_list.get(key), free_syncry_gpt_list.get(key), free_gpt_list.get(key), free_thermo_syncry_gpt_list.get(key), free_thermo_gpt_list.get(key)]

df = pd.DataFrame.from_dict(integrated_dic, orient='index', columns=['U-score_original', 'atom_syncry_gpt', 'atom_gpt', 'atom_thermo_syncry_gpt', 'atom_thermo_gpt', 'free_syncry_gpt', 'free_gpt', 'free_thermo_syncry_gpt', 'free_thermo_gpt'])
print(df.head())

with open("./integrated_results.json", 'w') as f:
    json.dump(integrated_dic, f, indent=4)

# after making this dataframe, you can analyze the results with various methods