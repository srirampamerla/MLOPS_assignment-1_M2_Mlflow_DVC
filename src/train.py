import pandas as pd
import warnings
import sys
warnings.filterwarnings("ignore")
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import mlflow
import mlflow.sklearn
from urllib.parse import urlparse
from mlflow.models import infer_signature
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

# Define evaluation metrics
def eval_metrics(actual, predicted):
    mse = mean_squared_error(actual, predicted)
    mae = mean_absolute_error(actual, predicted)
    r2 = r2_score(actual, predicted)
    return mse, mae, r2

# Load the dataset
try:
    data = pd.read_csv("data/housing.csv")
    logging.info("Dataset loaded successfully.")
except Exception as e:
    logging.error(f"Error loading dataset: {e}")
    raise

# Define features and target
X = data.drop(columns=["PRICE"])  # Replace 'target' with your target column name
y = data["PRICE"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
logging.info("Dataset split into training and testing sets.")

# Hyperparameter configurations for multiple runs
alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5



# Start MLflow experiment
mlflow.set_experiment("ElasticNet Regression")


with mlflow.start_run():
    try:
        # Initialize and train the Elastic Net model
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        model.fit(X_train, y_train)
        logging.info(f"Model training completed for alpha={alpha}, l1_ratio={l1_ratio}.")

        # Make predictions
        predictions = model.predict(X_test)
        signature = infer_signature(X_test, predictions) #Captures the schema of the input data (X_test) and the model's predictions. This is useful for validating data when deploying the model or serving predictions.

        # Evaluate the model
        mse, mae, r2 = eval_metrics(y_test, predictions)
        # Tracking
        # Log metrics to MLflow
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)

        # Log model parameters
        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        # Model registry does not work with file store
        if tracking_url_type_store != "file":
            # Register the model
            # There are other ways to use the Model Registry, which depends on the use case,
            # please refer to the doc for more information:
            # https://mlflow.org/docs/latest/model-registry.html#api-workflow
            mlflow.sklearn.log_model(
                model, "model", registered_model_name=f"ElasticNetModel_alpha_{alpha}_l1_{l1_ratio}"
                )

        else:
            mlflow.sklearn.log_model(model, "model")

        # # Log the trained model
        # mlflow.sklearn.log_model(model, "model")

        # Print evaluation results
        logging.info(f"ElasticNet model (alpha={alpha}, l1_ratio={l1_ratio}):")
        logging.info(f"Mean Squared Error (MSE): {mse:.2f}")
        logging.info(f"Mean Absolute Error (MAE): {mae:.2f}")
        logging.info(f"R² (Coefficient of Determination): {r2:.2f}")

    except Exception as e:
        logging.error(f"Error during model training or evaluation for alpha={alpha}, l1_ratio={l1_ratio}: {e}")
        raise
