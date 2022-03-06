tag="--->"

echo "$tag Write dependencies to requirements.txt..."
pipenv lock -r > requirements.txt

echo "$tag Download them into libs folder..."
python3 -m pip download --destination-directory ./src/cobthad/libs -r requirements.txt --no-binary=:all:
