#!/bin/bash

THIS_DIR=$(dirname "$0")
PROJECT_DIR=$(dirname "$THIS_DIR")
cd $PROJECT_DIR && python -m build