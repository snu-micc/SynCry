import jsonlines
import json

with open(".//(GPT)total_results.json", "r") as f:
    data_GPT = json.load(f)

with open(".//(PU-GPT)total_results.json", "r") as f:
    data_PU_GPT = json.load(f)

original_structure_GPT = []
modified_structure_GPT = []
original_structure_PU_GPT = []
modified_structure_PU_GPT = []

for i in range(11753):
    if data_GPT[i]["loop6_score"] > 0.852:
        original_structure_GPT.append(data_GPT[i]["original_structure"])
        modified_structure_GPT.append(data_GPT[i]["loop6_structure"])
    if data_PU_GPT[i]["loop6_score"] > 0.852:
        original_structure_PU_GPT.append(data_PU_GPT[i]["original_structure"])
        modified_structure_PU_GPT.append(data_PU_GPT[i]["loop6_structure"])

GPT_prompt = []
PU_GPT_prompt = []

for i in range(len(original_structure_GPT)):
    if original_structure_GPT[i] != modified_structure_GPT[i] and original_structure_GPT[i].count(" ") == modified_structure_GPT[i].count(" "): 
        request= {}
        request["messages"] = [
            { "role":"user", "content": "You are an expert inorganic chemist. Please demonstrate a modified structure representation(only one) that is thermodynamically stable(E_hull =near zero) and synthesizable for the following inorganic compound, which has been predicted as unlikely to be synthesized. You must respond in the exactly same format of 'a,b,c,alpha,beta,gamma: Atom0(coordinate), Atom1(coordinate)...' without any additional informations. Only modify the lattice parameters(a,b,c,alpha,beta.gamma) and atomic coordinates. DO NOT alter the atomic types or composition:" + original_structure_GPT[i] },
            { "role":"assistant", "content": modified_structure_GPT[i] }
        ]
        GPT_prompt.append(request)

for i in range(len(original_structure_PU_GPT)):
    if original_structure_PU_GPT[i] != modified_structure_PU_GPT[i] and original_structure_PU_GPT[i].count(" ") == modified_structure_PU_GPT[i].count(" "):
        request= {}
        request["messages"] = [
            { "role":"user", "content": "You are an expert inorganic chemist. Please demonstrate a modified structure representation(only one) that is thermodynamically stable(E_hull =near zero) and synthesizable for the following inorganic compound, which has been predicted as unlikely to be synthesized. You must respond in the exactly same format of 'a,b,c,alpha,beta,gamma: Atom0(coordinate), Atom1(coordinate)...' without any additional informations. Only modify the lattice parameters(a,b,c,alpha,beta.gamma) and atomic coordinates. DO NOT alter the atomic types or composition:" + original_structure_PU_GPT[i] },
            { "role":"assistant", "content": modified_structure_PU_GPT[i] }
        ]
        PU_GPT_prompt.append(request)


with open(".//LOOP6//FT_for_LOOP7//train_data_GPT.jsonl", encoding="utf-8", mode="w") as f:
    for i in GPT_prompt:
        f.write(json.dumps(i) + "\n")

with open(".//LOOP6//FT_for_LOOP7//train_data_PU_GPT.jsonl", encoding="utf-8", mode="w") as f:
    for i in PU_GPT_prompt:
        f.write(json.dumps(i) + "\n")


