export version=latest
docker build . -t builder
docker create -ti --name builder IMAGE_NAME builder
docker cp builder:.python_packages ./Functions/.
cd Functions
zip -9 -r -x=*.DS_Store* -x=published/ -x=local.settings.json -x=*.sh -x=*.dat -x=.funcignore -x="*venv/*" -x=*__pycache__* published/$version-build.zip .