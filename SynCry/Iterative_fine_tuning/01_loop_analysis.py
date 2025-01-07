import jsonlines
import json
import math

# we provide the code example for the loop7 analysis

#information about scores
with open(".//LOOP7//results_prediction//formatted_SynCry-GPT.json", "r") as f:
    syncry_gpt = json.load(f)
with open(".//LOOP7//results_prediction//formatted_GPT.json", "r") as f:
    GPT = json.load(f)

GPT_structure = []
syncry_gpt_structure = []

#information about structures
with jsonlines.open(".//LOOP7//results_modification//GPT.jsonl", "r") as f:
    for lines in f.iter():
        GPT_structure.append(lines['response']['body']['choices'][0]['message']['content'])

with jsonlines.open(".//LOOP7//results_modification//SynCry-GPT.jsonl", "r") as f:
    for lines in f.iter():
        syncry_gpt_structure.append(lines['response']['body']['choices'][0]['message']['content'])

GPT_result = {}
syncry_gpt_result ={}
error_count = 0

if 'gpt' in syncry_gpt[0]['Model']:
    for i, pred in enumerate(syncry_gpt):
        try:
            p_check = "U"
            if pred["Prediction1"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs1"])
                p_check = "P"
            elif pred["Prediction2"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs2"])
            elif pred["Prediction3"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs3"])
            syncry_gpt_result[f"{pred['custom_id']}"] = p_score
        except:
            error_count += 1
            syncry_gpt_result[f"{pred['custom_id']}"] = [0]

if 'gpt' in GPT[0]['Model']:
    for i, pred in enumerate(GPT):
        try:
            p_check = "U"
            if pred["Prediction1"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs1"])
                p_check = "P"
            elif pred["Prediction2"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs2"])
            elif pred["Prediction3"] in ['P', 'Y', ' P', 'Yes', 'p', '"P', 'Possible']:
                p_score = math.exp(pred["Logprobs3"])
            GPT_result[f"{pred['custom_id']}"] = p_score
        except:
            error_count += 1
            GPT_result[f"{pred['custom_id']}"] = [0]

score_syncry_gpt = []
score_GPT=[]

for i in range(len(syncry_gpt_result)):
    score_syncry_gpt.append(syncry_gpt_result[f"request-{i+1}"])

for i in range(len(GPT_result)):
    score_GPT.append(GPT_result[f"request-{i+1}"])

count_syncry_gpt = sum(1 for score in score_syncry_gpt if score > 0.852)
count_GPT = sum(1 for score in score_GPT if score > 0.852)

print(f"Count of syncry_gpt scores over 0.852: {count_syncry_gpt}") #loop0: 514, loop1: 1262, loop2: 1650, loop3: 2006, loop4: 2442, loop5:3109, loop6: 3175, loop7: 3395
print(f"Count of GPT scores over 0.852: {count_GPT}") #loop0: 434, loop1: 1081, loop2: 1379, loop3: 1608, loop4: 1768, loop5: 1982, loop6: 2061, loop7: 2157

# we save this to the total_results.json file

with open(".//(GPT)total_results.json", "r") as f:
    data_GPT = json.load(f)

for i in range(11753):
    data_GPT[i]["loop7_structure"] = GPT_structure[i]
    data_GPT[i]["loop7_score"] = score_GPT[i]

with open(".//(GPT)total_results.json", "w") as f:
    json.dump(data_GPT, f, indent=4)

with open(".//(SynCry-GPT)total_results.json", "r") as f:
    data_syncry_gpt = json.load(f)

for i in range(11753):
    data_syncry_gpt[i]["loop7_structure"] = syncry_gpt_structure[i]
    data_syncry_gpt[i]["loop7_score"] = score_syncry_gpt[i]
    

with open(".//(SynCry-GPT)total_results.json", "w") as f:
    json.dump(data_syncry_gpt, f, indent=4)