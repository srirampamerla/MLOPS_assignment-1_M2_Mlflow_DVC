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

4. Remote Tracking with DAGsHub

Preparation

Push your code to GitHub (omit the mlruns folder).

Log in to DAGsHub and link your repository.

Environment Variables

In Git Bash, set the required environment variables:

```
export MLFLOW_TRACKING_URI="your_dagshub_tracking_uri"
export MLFLOW_TRACKING_USERNAME="your_username"
export MLFLOW_TRACKING_PASSWORD="your_password"
```
Modify Code for Remote Tracking
Add these lines to point to the remote server:
```
remote_server_uri = "your_dagshub_tracking_uri"
mlflow.set_tracking_uri(remote_server_uri)
```
Run the Script

Execute your script:
```
python your_script.py
```
The mlruns folder will be directly created in DAGsHub. You can explore the results under:

Repository → Experiments on the DAGsHub interface.

5. Visualization and Comparison

On DAGsHub or the MLflow UI:

Select multiple runs for comparison.

Visualize metrics and parameters to identify trends and performance differences.

Use artifacts to retrieve and deploy models.

# DVC

1. Setup DVC and Git
2. 
Install DVC in your environment:

```
pip install dvc
```
Initialize Git Repository

```
git init
```
Initialize DVC
```
dvc init
```
This creates a .dvc/ directory containing configuration files for DVC.

Adds .dvcignore to specify files or directories that DVC should not track.

Use Git to track these initial files:

```
git add .dvc .dvcignore
git commit -m "Initialize DVC"
```
2. Track Data Files with DVC

To start tracking a data file (e.g., data/data.csv):
```
dvc add data/data.csv
```
This creates:

data.csv.dvc: A metafile with a hash key and metadata for data.csv.

Adds the path of data.csv to .gitignore.

Use Git to Track DVC Metadata
```
git add data/data.csv.dvc data/.gitignore
git commit -m "Track data file with DVC"
```
3. Manage Updates to Data Files

If you modify data.csv, run:
```
dvc add data/data.csv
```
This updates the hash key in data.csv.dvc.

Use Git to track the changes:

```
git add data/data.csv.dvc
git commit -m "Update data file"
```

4. Switch Between Data Versions

To move between versions:

Use Git to checkout a specific commit:
```
git checkout <commit-id>
```

Update the working data file to match the DVC version:

```
dvc checkout
```

This ensures data/data.csv reflects the version specified in data.csv.dvc.

Return to the Latest Version

Switch back to the main branch:
```
git checkout main
dvc checkout
```

5. Check Logs and Branches

Use git log to view the history of changes.

Create branches to manage different versions of your project:

```
git branch <branch-name>
```

6. DVC Cache and Optimization

DVC stores the actual file content in .dvc/cache/ with hash keys based on file content.

If two versions of a file share the same content, DVC efficiently stores it once.










