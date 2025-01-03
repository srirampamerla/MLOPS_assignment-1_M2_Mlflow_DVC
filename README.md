# MLFLOW
**Implementation Steps**
**1. Experiment Tracking with MLflow**

Step 1: Set Up MLflow & Install

```
pip install mlflow==2.19.0
```
2. Set Up MLflow in Your Code
Experiment Initialization

```
import mlflow
from mlflow.models import infer_signature

# Set experiment name
mlflow.set_experiment("Your_Experiment_Name")

# Start an MLflow run
with mlflow.start_run():
    # Your code for training and evaluation goes here
    ...
```

Tracking URL Type
This identifies whether MLflow is using a local file or remote server for storing experiments:

```
from urllib.parse import urlparse

tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme\

```
Log Metrics, Parameters, and Model
To track your model's performance and configuration:
```
mlflow.log_metric("mse", mse)
mlflow.log_param("alpha", alpha)
mlflow.sklearn.log_model(model, "model", registered_model_name="Your_Model_Name", signature=infer_signature(X_test, predictions))
```
3. Local MLflow UI
When you run your script, an mlruns folder is created locally, containing:

Artifacts: Model files, metrics, parameters, and more.
conda.yml: Captures dependencies.
Model Files: Serialized versions of the model.
To view these runs in the MLflow UI:
```
mlflow ui
```
Navigate to http://localhost:5000 in your browser to explore:

Experiment details
Run comparisons
Visualizations

**Remote Purpose**

push all the code except mlruns into github.

Open dagshub and login and try to link the git folder.

export the mlflow_tracking_uri, mlflow_tracking_username, mlflow_tracking_password in git bash

for remote purpose we will add 2 lines in code.
remote_server_uri='mlflow_tracking_uri id'
mlflow.set_tracking_uri(remore_server_uri)

Run the script in bash folder(python file.py)

Now the ML run folder that will probably get created.

Go to dagshub->Repository-> experiments-> We can see our ml run.



It will directly get created in the DAGs hub uh URL right.





