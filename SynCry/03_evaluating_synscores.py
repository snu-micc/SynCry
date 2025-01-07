from openai import OpenAI
import jsonlines
import json

# do this for 8 types of prompts if you are undergoing the prompt engineering process
modified_structures = []
file_name = ""
with jsonlines.open(file_name) as f:
    for line in f.iter():
        modified_structures.append(line['response']['body']['choices'][0]['message']['content'])

batch_data = []
for i in range(len(modified_structures)):
    request = {}
    request["custom_id"] = "request-"+str(i+1)
    request["method"] = "POST"
    request["url"] = "/v1/chat/completions"
    request["body"] = {
                       "model": "ft:gpt-4o-mini-2024-07-18:micc:cifstringsonly:A5WfVdjl",
                       "temperature": 0,
                       "logprobs": True,
                       "top_logprobs": 3,
                       "max_tokens": 2,
                       # below prompt is same as StructLLM's prompt, which is our baseline work for synthesizability prediction
                       "messages": [
                           {"role":"system", "content": "You are an expert inorganic chemist.  Determine if the following compound is likely to be synthesizable based on its structural description, answering only \"P\" (for positive or possible) and \"U\" (for unknown or unlikely). "},
                           {"role":"user", "content": "Is this inorganic compound synthesizable? : "+ modified_structures[i]},
                       ],
                       }
    batch_data.append(request)

with open(file_name[:-6]+"_prediction_batch.jsonl", encoding= "utf-8",mode="w") as file:
        file.write(json.dumps(i) + "\n")
