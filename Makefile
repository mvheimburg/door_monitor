#################################################
## Makefile for dev env generation         ## 
#################################################

.PHONY: dev
dev: venv
	$(VENV)/python3 -m gui



include Makefile.venv