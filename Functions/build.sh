export version=v1
zip -9 -r -x=*.DS_Store* -x=published/* -x=local.settings.json -x=*.sh -x=*.dat -x=.funcignore -x="*venv/*" -x=*__pycache__* published/$version-build.zip . 