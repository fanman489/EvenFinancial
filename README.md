# EvenFinancia

Main.py: Script for data pipeline and model training and evaluation. 

  The Main.py script accesses the following:
  1. DataProcessing.py: Contains functions for data processing
  2. SQLPipeline.py: Class to connect to and read/write from the PostgresSQL database.
  3. Models.py: Class that contains the logistic regression model.
  4. utils.py: Utility functions


App.py: The webapp script. See the documentation for details on running. This script references the Models.py script which contains the trained model.
