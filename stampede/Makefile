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
	sbatch -J cmtmrsa -p development -t 02:00:00 ./run.sh -q $(WORK)/data/bugs/mssa_mrsa/ -o $(WORK)/data/bug/commet-mrsa 
