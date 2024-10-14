Skip to content
Navigation Menu
LLMforTDD
/
LLMforTDD

Type / to search
Code
Issues
2
Pull requests
1
Actions
Projects
Security
Insights
Comparing changes
Choose two branches to see what’s changed or to start a new pull request. If you need to, you can also  or learn more about diff comparisons.
 
 
...
 
 
  Able to merge. These branches can be automatically merged.
 Create Gemini.py #4
No description available
 1 commit
 1 file changed
 1 contributor
Commits on Oct 15, 2024
Create Gemini.py

@AlagarsamySaranya
AlagarsamySaranya authored 2 minutes ago
 Showing  with 101 additions and 0 deletions.
 101 changes: 101 additions & 0 deletions101  
Gemini.py
Original file line number	Diff line number	Diff line change
@@ -0,0 +1,101 @@
import googleapiclient.discovery
import json
import time
import pandas as pd

# Initialize the AI Platform client
client = googleapiclient.discovery.build('aiplatform', 'v1')

# Define the project and location
project_id = 'your-project-id' # we can get this by creating the api
location = 'us-central1'

# Load the training and test datasets
train_file = 'training.csv'
test_file = 'test.csv'

df_train = pd.read_csv(train_file)
df_test = pd.read_csv(test_file)

# Define columns
input_column = 'Description'
output_column = 'test_case'
method_column = 'Method'


fine_tuning_data = []

for i in range(len(df_train)):
    description_content = df_train[input_column][i]
    test_case = df_train[output_column][i]
    method = df_train[method_column][i]
    method_data_with_description = {method: f"{method_descriptions[method]}: {df_train[method][i]}" for method in methods}
    fine_tuning_data.append({
        "prompt": f"Method: {method}\nDescription: {description_content}\nmethods: {json.dumps(method_data_with_description)}\nTest Case:",
        "completion": test_case
    })

# Create a tuning job
tuning_job = client.projects().locations().customJobs().create(
    parent=f'projects/{project_id}/locations/{location}',
    body={
        'displayName': 'gemini-fine-tune-job',
        'jobSpec': {
            'workerPoolSpecs': [
                {
                    'machineSpec': {
                        'machineType': 'n1-standard-4'
                    },
                    'replicaCount': 1,
                    'containerSpec': {
                        'imageUri': 'gcr.io/your-project-id/gemini-tuning-container',
                        'args': ['--training_data', json.dumps(fine_tuning_data)]
                    }
                }
            ]
        }
    }
).execute()

print('Tuning job created:', tuning_job)

# Wait for the tuning job to complete
job_name = tuning_job['name']
while True:
    job = client.projects().locations().customJobs().get(name=job_name).execute()
    if job['state'] == 'SUCCEEDED':
        print('Tuning job completed successfully.')
        break
    elif job['state'] == 'FAILED':
        print('Tuning job failed.')
        break
    else:
        print('Tuning job in progress...')
        time.sleep(60)

# Retrieve the model ID from the completed job
model_id = job['model']

# Prepare the test data for inference
inference_data = []

for i in range(len(df_test)):
    method = df_test[method_column][i]
    description_content = df_test[input_column][i]
    method_data_with_description = {method: f"{method_descriptions[method]}: {df_test[method][i]}" for method in methods}
    inference_data.append({
        'input': f"Method: {method}\nDescription: {description_content}\nmethods: {json.dumps(method_data_with_description)}\nTest Case:"
    })

# Use the fine-tuned model for inference
request_body = {
    'instances': inference_data
}

response = client.projects().locations().models().predict(
    name=f'projects/{project_id}/locations/{location}/models/{model_id}',
    body=request_body
).execute()

# Print the response
print(json.dumps(response, indent=2))
Footer
© 2024 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact
Manage cookies
Do not share my personal information
