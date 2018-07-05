SINGULARITY = /usr/local/bin/singularity
IMG_NAME = commet-0.1.0.img
DEF_NAME = image.def
SIZE = 1024

run:
	sudo $(SINGULARITY) run $(IMG_NAME)

clean:
	rm -f $(IMG_NAME)

img: clean
	#sudo $(SINGULARITY) build $(IMG_NAME) $(DEF_NAME)
	sudo $(SINGULARITY) create --size $(SIZE) $(IMG_NAME)
	sudo $(SINGULARITY) bootstrap $(IMG_NAME) $(DEF_NAME)

shell:
	sudo $(SINGULARITY) shell --writable -B $(HOME):/home1 -B /data:/work $(IMG_NAME)

pooled:
	sudo $(SINGULARITY) exec -B $(HOME):/home1 -B /data:/work $(IMG_NAME) run.py
