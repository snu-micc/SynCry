import jsonlines
import json

#This code is how we pre-process the prediction batch result file to our result format

batch_test = []
with jsonlines.open("") as f: # load the batch result file for synthesizability score prediction
    for line in f.iter():
        batch_test.append(line)

prediction_result = []
for i in range(len(batch_test)):
    d_idx = int(batch_test[i]['custom_id'].split('request-')[-1])-1
    response = batch_test[i]['response']
    pred_result = {}
    pred_result['Model'] = response['body']['model']
    pred_result['custom_id'] = batch_test[i]['custom_id']
    pred_result['Prediction1'] = response['body']['choices'][0]['logprobs']['content'][0]['top_logprobs'][0]['token']
    pred_result['Prediction2'] = response['body']['choices'][0]['logprobs']['content'][0]['top_logprobs'][1]['token']
    pred_result['Prediction3'] = response['body']['choices'][0]['logprobs']['content'][0]['top_logprobs'][2]['token']
    pred_result['Logprobs1'] = response['body']['choices'][0]['logprobs']['content'][0]['top_logprobs'][0]['logprob']
    pred_result['Logprobs2'] = response['body']['choices'][0]['logprobs']['content'][0]['top_logprobs'][1]['logprob']
    pred_result['Logprobs3'] = response['body']['choices'][0]['logprobs']['content'][0]['top_logprobs'][2]['logprob']
    prediction_result.append(pred_result)

save_path = "./prediction_results/batch_data_formatted/"
with open(save_path+"", 'w') as f: # save the prediction result in a json file
    json.dump(prediction_result, f, indent=4)

