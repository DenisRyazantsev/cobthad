tag="--->"

echo "$tag Update dependencies..."
pipenv update

echo "$tag Move all dependencies to requirements.py..."
pipenv lock -r > requirements.txt

echo "$tag Move all dependencies to setup.py..."
pipenv-setup sync

echo "$tag Download them into libs folder..."
python -m pip download --destination-directory ./src/libs -r requirements.txt --no-binary=:all:
