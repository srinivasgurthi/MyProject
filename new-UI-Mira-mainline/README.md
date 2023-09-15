# auto-cafe-template

# update Python path
export PYTHONPATH=$PYTHONPATH:/<path to your autmation folder>  


Code Setup
==========


virtualenv venv
source venv/bin/activate 
pip install -r requirements.txt

#export your env file 

pytest automation/tests/ui/test.py --env=pavo