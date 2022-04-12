all: README.md
%: temp_% harddisk.py LennardJones.py
	-cp $< $@.1
	for f in harddisk.py LennardJones.py; do python3 $$f -h | python3 Utilities/replace.py %%usage-$$f%% "    " $@.1 > $@.2; mv $@.2 $@.1;done
	mv $@.1 $@
makeenv:
	cd ~/venvs; python3 -m venv pygame

pep8:
	autopep8 -r -a -a -i .
