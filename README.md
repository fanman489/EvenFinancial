# PredictClick

Main.py: Script for data pipeline, model training, and evaluation. 

  The Main.py script accesses the following:
  1. DataProcessing.py: Contains functions for data processing
  2. SQLPipeline.py: Class to connect to and read/write from the PostgresSQL database.
  3. Models.py: Class that contains the logistic regression model and all functions related to training.
  4. utils.py: Utility functions


App.py: The webapp script. See the documentation for details on running. This script uses a trained model from the Models.py script.
