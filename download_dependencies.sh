tag="--->"

echo "$tag Write dependencies to requirements.txt..."
pipenv lock -r > requirements.txt

echo "$tag Download them into libs folder..."
pip install -r requirements.txt -t "./src/cobthad/libs" --no-binary=:all:
