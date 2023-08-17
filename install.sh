#!/bin/bash

# Install dependency + save new requirements.txt

pip install $1
./freeze.sh