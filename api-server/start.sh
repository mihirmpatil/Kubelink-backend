#! /bin/bash
export PATH=$PATH:/usr/src/app
# Set context to service catalog
./service-catalog-context.sh


# Start flask server
python main.py
