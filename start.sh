#!/bin/bash
# Start the Python Fraud API in the background
python fraud_api.py &

# Start the Node.js server in the foreground
node server.js
