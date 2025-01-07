from openai import OpenAI

# This procedure is both applicable for 02 and 03 codes, uploading the batch request file to openAI server. You can do this manually, but it is better to automate this process. 

# 1. Your openai api key
client = OpenAI(api_key="") 


# 2. Uploading Your Batch Input File(Iterate for each request)
batch_input_file = client.files.create(
  file=open("", "rb"),
  purpose="batch"
)

# 3. Creating the Batch
batch_input_file_id = batch_input_file.id

client.batches.create(
    input_file_id=batch_input_file_id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
      "description": "nightly eval job"
    }
)


# 4. Checking the Status of a Batch
#client.batches.retrieve('batch_xxxxxxxxxxxx')


# 5. Retrieving the Results
#content = client.files.content("file-yyyyyyyyyyyy")
# 6. Download the batch_result (e.g. batch_xxxxxxxxxxxxxxx_output.jsonl)
# 7. using "batchresult2resultformat.py" to convert batch result to our result formmat.