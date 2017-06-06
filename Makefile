.PHONY: clean
clean:
	- rm -rf env
	- find . -name "*.pyc" | xargs rm

env/bin/activate: requirements.txt requirements-dev.txt
	virtualenv --python=python3.6 env
	. env/bin/activate && pip install -r requirements.txt -r requirements-dev.txt

.PHONY: requirements
requirements: env/bin/activate

.PHONY: lint
lint:
	. env/bin/activate && flake8 bigbother

.PHONY: infrastructure
infrastructure: requirements lint
	. env/bin/activate && stacker build \
		-t \
		-r eu-west-2 \
		cloudformation/config/bigbother.env \
		cloudformation/config/bigbother.yaml
