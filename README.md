This repository contains helpers scripts to interface with my dissertation evaluation. 

# geth_db

Predominantely a python project used to create test data, run a test script and create a flask server around a python-geth instance.

## Flask server (run_geth_db.py)

The flask server contained in geth_db is used to create and interface with a python-geth instance and act as our GethDB for our evaluation. 

`run_geth_db.py` is the entrypoint. 

## run_test.py

A script to run the tests. It runs several requests to both a Mongo and GethDB implementation

## db

Holds the contract and utility functions to interface with the contract

## create_mass_data.py

Creates test data

# server_mongo

Is an ExpressJS project with an example layout of a controller, service and db(models) instances to interface with MongoDB. 



