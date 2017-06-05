.PHONY: clean
clean:
	- rm -rf env
	- find . -name "*.pyc" | xargs rm

env/bin/activate:
	virtualenv --python=python3.6 env

requirements.txt: env/bin/activate
	. env/bin/activate && pip install -r requirements.txt

.PHONY: lint
lint:
	. env/bin/activate && flake8 bigbother

.PHONY: infrastructure
infrastructure: requirements.txt lint
	. env/bin/activate && stacker build \
		-t \
		-r eu-west-2 \
		cloudformation/config/bigbother.env \
		cloudformation/config/bigbother.yaml
