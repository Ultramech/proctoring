#!/bin/bash
set -o errexit

echo "Installing Standard Requirements..."
pip install -r requirements.txt

echo "Installing Dlib (Pre-compiled)..."
pip install dlib-bin

echo "Installing Face Recognition (No Deps)..."
pip install face-recognition==1.3.0 --no-deps

echo "Collecting Static Files..."
python manage.py collectstatic --noinput
