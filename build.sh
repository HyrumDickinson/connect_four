# deactivate venv
venv deactivate

# delete the previous packages
rm -r dist

# build the packages
python3 -m pip install build twine
python3 -m build

# automatically look for issues in the build
twine check dist/*

# manually verify that they were built correctly
cd dist/
unzip grade_calculator-0.0.0-py3-none-any.whl -d grade_calculator.whl # update version numbering as necessary
tree grade_calculator.whl/

# reactivate venv
venv source/bin/activate