APP = commet-0.l.0
EMAIL = kyclark@email.arizona.edu

clean:
	find . \( -name \*.out -o -name \*.param \) -exec rm {} \;

up: 
	copy_from_manifest.py

template:
	jobs-template -A $(APP) > job.json

job:
	jobs-submit -F job.json

app:
	apps-addupdate -F app.json

test: clean
	sbatch test.sh

mrsa:
	sbatch -J cmtmrsa ./run.sh -q $(WORK)/data/bugs/mssa_mrsa/ -o $(WORK)/data/bugs/commet-mrsa 

lakea:
	sbatch -J lakea ./run.sh -q $(WORK)/myriam/filtered -o $(WORK)/myriam/commet-out
