import json
import jsonlines
import math

#1. extraction of U-structures

u_structure_custom_ids = []
u_structure_lists = []
u_score_lists = []

with jsonlines.open("", 'r') as f: # your data path
    for line in f.iter():
        if line['response']['body']['choices'][0]['logprobs']['content'][0]['top_logprobs'][0]['token'] == 'U':
            u_structure_custom_ids.append(line['custom_id'])
            u_score_lists.append(math.exp(line['response']['body']['choices'][0]['logprobs']['content'][0]['top_logprobs'][1]['logprob']))

with jsonlines.open("", 'r') as f: # your data path
    for line in f.iter():
        if line['custom_id'] in u_structure_custom_ids:
            u_structure_lists.append(line['body']['messages'][1]['content'].split(":")[1]+":"+line['body']['messages'][1]['content'].split(":")[2])

with jsonlines.open("", 'w') as f: # your data path
    for i, j in zip(u_structure_lists, u_score_lists):
        f.write({"u_structure": i, "u_score": j})

u_data = "" # your u_data path


# 8 types of prompts demonstrated in the Figure S3. FT = SynCry-GPT and GPT = GPT-4o-mini.
requests_free_FT = []
requests_atom_FT = []
requests_free_thermo_FT = []
requests_atom_thermo_FT = []
requests_free_GPT = []
requests_atom_GPT = []
requests_free_thermo_GPT = []
requests_atom_thermo_GPT = []

count=1
for i in u_structure_lists:
    request = {}
    request["custom_id"] = "request-"+str(count)
    count+=1
    request["method"] = "POST"
    request["url"] = "/v1/chat/completions"
    request["body"] = {
        "model": "ft:gpt-4o-mini-2024-07-18:micc:cifstringsonly:A5WfVdjl",
        "temperature": 0,
        "max_tokens": 1000,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert inorganic chemist. Please demonstrate a modified structure representation(only one) that is synthesizable for the following inorganic compound, which has been predicted as unlikely to be synthesized. You must respond in the exactly same format of 'a,b,c,alpha,beta,gamma: Atom0(coordinate), Atom1(coordinate)...' without any additional informations. Only modify the lattice parameters(a,b,c,alpha,beta,gamma) and atomic coordinates. DO NOT alter the atomic types or composition:"
            },
            {
                "role": "user",
                "content": "A structure predicted as unlikely to be synthesized : "+str(i)
            }
        ]
    }
    requests_free_FT.append(request)

count=1
for i in u_structure_lists:
    request = {}
    request["custom_id"] = "request-"+str(count)
    count+=1
    request["method"] = "POST"
    request["url"] = "/v1/chat/completions"
    request["body"] = {
        "model": "ft:gpt-4o-mini-2024-07-18:micc:cifstringsonly:A5WfVdjl",
        "temperature": 0,
        "max_tokens": 1000,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert inorganic chemist. Please demonstrate a modified structure representation(only one) that is synthesizable for the following inorganic compound, which has been predicted as unlikely to be synthesized. You must respond in the exactly same format of 'a,b,c,alpha,beta,gamma: Atom0(coordinate), Atom1(coordinate)...' without any additional informations. Only modify the atomic coordinates. DO NOT alter the lattice parameters(a,b,c,alpha,beta,gamma), atomic types or composition:"
            },
            {
                "role": "user",
                "content": "A structure predicted as unlikely to be synthesized : "+str(i)
            }
        ]
    }
    requests_atom_FT.append(request)

count=1
for i in u_structure_lists:
    request = {}
    request["custom_id"] = "request-"+str(count)
    count+=1
    request["method"] = "POST"
    request["url"] = "/v1/chat/completions"
    request["body"] = {
        "model": "ft:gpt-4o-mini-2024-07-18:micc:cifstringsonly:A5WfVdjl",
        "temperature": 0,
        "max_tokens": 1000,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert inorganic chemist. Please demonstrate a modified structure representation(only one) that is thermodynamically stable(E_hull = near zero) and synthesizable for the following inorganic compound, which has been predicted as unlikely to be synthesized. You must respond in the exactly same format of 'a,b,c,alpha,beta,gamma: Atom0(coordinate), Atom1(coordinate)...' without any additional informations. Only modify the lattice parameters(a,b,c,alpha,beta,gamma) and atomic coordinates. DO NOT alter the atomic types or composition:"
            },
            {
                "role": "user",
                "content": "A structure predicted as unlikely to be synthesized : "+str(i)
            }
        ]
    }
    requests_free_thermo_FT.append(request)

count=1
for i in u_structure_lists:
    request = {}
    request["custom_id"] = "request-"+str(count)
    count+=1
    request["method"] = "POST"
    request["url"] = "/v1/chat/completions"
    request["body"] = {
        "model": "ft:gpt-4o-mini-2024-07-18:micc:cifstringsonly:A5WfVdjl",
        "temperature": 0,
        "max_tokens": 1000,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert inorganic chemist. Please demonstrate a modified structure representation(only one) that is thermodynamically stable(E_hull =near zero) and synthesizable for the following inorganic compound, which has been predicted as unlikely to be synthesized. You must respond in the exactly same format of 'a,b,c,alpha,beta,gamma: Atom0(coordinate), Atom1(coordinate)...' without any additional informations. Only modify the atomic coordinates. DO NOT alter the lattice parameters(a,b,c,alpha,beta,gamma), atomic types or composition:"
            },
            {
                "role": "user",
                "content": "A structure predicted as unlikely to be synthesized : "+str(i)
            }
            # atom 위치만 바꾸는것 ( 결정 parameter 들은 유지하고 )
        ]
    }
    requests_atom_thermo_FT.append(request)

# same for GPT

count=1
for i in u_structure_lists:
    request = {}
    request["custom_id"] = "request-"+str(count)
    count+=1
    request["method"] = "POST"
    request["url"] = "/v1/chat/completions"
    request["body"] = {
        "model": "gpt-4o-mini-2024-07-18",
        "temperature": 0,
        "max_tokens": 1000,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert inorganic chemist. Please demonstrate a modified structure representation(only one) that is synthesizable for the following inorganic compound, which has been predicted as unlikely to be synthesized. You must respond in the exactly same format of 'a,b,c,alpha,beta,gamma: Atom0(coordinate), Atom1(coordinate)...' without any additional informations. Only modify the lattice parameters(a,b,c,alpha,beta,gamma) and atomic coordinates. DO NOT alter the atomic types or composition:"
            },
            {
                "role": "user",
                "content": "A structure predicted as unlikely to be synthesized : "+str(i)
            }
        ]
    }
    requests_free_GPT.append(request)

count=1
for i in u_structure_lists:
    request = {}
    request["custom_id"] = "request-"+str(count)
    count+=1
    request["method"] = "POST"
    request["url"] = "/v1/chat/completions"
    request["body"] = {
        "model": "gpt-4o-mini-2024-07-18",
        "temperature": 0,
        "max_tokens": 1000,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert inorganic chemist. Please demonstrate a modified structure representation(only one) that is synthesizable for the following inorganic compound, which has been predicted as unlikely to be synthesized. You must respond in the exactly same format of 'a,b,c,alpha,beta,gamma: Atom0(coordinate), Atom1(coordinate)...' without any additional informations. Only modify the atomic coordinates. DO NOT alter the lattice parameters(a,b,c,alpha,beta,gamma), atomic types or composition:"
            },
            {
                "role": "user",
                "content": "A structure predicted as unlikely to be synthesized : "+str(i)
            }
        ]
    }
    requests_atom_GPT.append(request)

count=1
for i in u_structure_lists:
    request = {}
    request["custom_id"] = "request-"+str(count)
    count+=1
    request["method"] = "POST"
    request["url"] = "/v1/chat/completions"
    request["body"] = {
        "model": "gpt-4o-mini-2024-07-18",
        "temperature": 0,
        "max_tokens": 1000,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert inorganic chemist. Please demonstrate a modified structure representation(only one) that is thermodynamically stable(E_hull = near zero) and synthesizable for the following inorganic compound, which has been predicted as unlikely to be synthesized. You must respond in the exactly same format of 'a,b,c,alpha,beta,gamma: Atom0(coordinate), Atom1(coordinate)...' without any additional informations. Only modify the lattice parameters(a,b,c,alpha,beta,gamma) and atomic coordinates. DO NOT alter the atomic types or composition:"
            },
            {
                "role": "user",
                "content": "A structure predicted as unlikely to be synthesized : "+str(i)
            }
        ]
    }
    requests_free_thermo_GPT.append(request)

count=1
for i in u_structure_lists:
    request = {}
    request["custom_id"] = "request-"+str(count)
    count+=1
    request["method"] = "POST"
    request["url"] = "/v1/chat/completions"
    request["body"] = {
        "model": "gpt-4o-mini-2024-07-18",
        "temperature": 0,
        "max_tokens": 1000,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert inorganic chemist. Please demonstrate a modified structure representation(only one) that is thermodynamically stable(E_hull =near zero) and synthesizable for the following inorganic compound, which has been predicted as unlikely to be synthesized. You must respond in the exactly same format of 'a,b,c,alpha,beta,gamma: Atom0(coordinate), Atom1(coordinate)...' without any additional informations. Only modify the atomic coordinates. DO NOT alter the lattice parameters(a,b,c,alpha,beta,gamma), atomic types or composition:"
            },
            {
                "role": "user",
                "content": "A structure predicted as unlikely to be synthesized : "+str(i)
            }
        ]
    }
    requests_atom_thermo_GPT.append(request)

save_dir = "" # your save path

with open(save_dir+"/requests_free_FT.jsonl" , encoding= "utf-8",mode="w") as file:
    for i in requests_free_FT:
        file.write(json.dumps(i) + "\n")
with open(save_dir+"/requests_atom_FT.jsonl" , encoding= "utf-8",mode="w") as file:
    for i in requests_atom_FT:
        file.write(json.dumps(i) + "\n")
with open(save_dir+"/requests_free_thermo_FT.jsonl" , encoding= "utf-8",mode="w") as file:
    for i in requests_free_thermo_FT:
        file.write(json.dumps(i) + "\n")
with open(save_dir+"/requests_atom_thermo_FT.jsonl" , encoding= "utf-8",mode="w") as file:
    for i in requests_atom_thermo_FT:
        file.write(json.dumps(i) + "\n")
with open(save_dir+"/requests_free_GPT.jsonl" , encoding= "utf-8",mode="w") as file:
    for i in requests_free_GPT:
        file.write(json.dumps(i) + "\n")
with open(save_dir+"/requests_atom_GPT.jsonl" , encoding= "utf-8",mode="w") as file:
    for i in requests_atom_GPT:
        file.write(json.dumps(i) + "\n")
with open(save_dir+"/requests_free_thermo_GPT.jsonl" , encoding= "utf-8",mode="w") as file:
    for i in requests_free_thermo_GPT:
        file.write(json.dumps(i) + "\n")
with open(save_dir+"/requests_atom_thermo_GPT.jsonl" , encoding= "utf-8",mode="w") as file:
    for i in requests_atom_thermo_GPT:
        file.write(json.dumps(i) + "\n")


