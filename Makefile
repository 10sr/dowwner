DOWWNER_ENV ?= local
DOWWNER_PORT ?= 9900
DOWWNER_HOST ?= 0.0.0.0

export DOWWNER_BASE_DIR := $(CURDIR)

MAKEFLAGS += --no-builtin-rules --no-builtin-variable

# https://stackoverflow.com/questions/10859916/how-to-treat-a-warning-as-an-error-in-a-makefile/29800774#29800774
MAKECMDGOALS ?= check
${MAKECMDGOALS}: fatal-on-warning
fatal-on-warning:
	@! (${MAKE} -n --warn-undefined-variables ${MAKECMDGOALS} 2>&1 >/dev/null | grep 'warning:')


app := app
project := dowwner

poetry := poetry

# TODO: Remove env from this command
python3 := ${poetry} run env DOWWNER_ENV=${DOWWNER_ENV} python3
manage_py := ${python3} ./manage.py

# Make all targets phony
.PHONY: $(MAKECMDGOALS)

check: poetry-check app-test mypy black-check

env:
	env

installdeps:
	${poetry} install

runserver:
	${manage_py} $@ '${DOWWNER_HOST}:${DOWWNER_PORT}'

# https://docs.djangoproject.com/en/1.10/intro/tutorial02/#database-setup
migrate:
	${manage_py} $@

# https://docs.djangoproject.com/en/1.10/intro/tutorial02/#activating-models
makemigrations:
	${manage_py} $@ ${app}

# Print sql query for migration
sqlmigrate:
	${manage_py} $@ ${app} ${target}

local_addrecords create_admin_user create_local_user:
	${manage_py} $@

shell:
	${manage_py} shell

manage_py:
	${manage_py} ${command}

poetry-check:
	${poetry} check

app-test:
	${manage_py} makemigrations --dry-run --check
	${python3} -Wa ./manage.py test tests/


###########
# Docker

docker-build:
	docker build . -t local/neru

# TODO: Add file like docker_local.env
docker-run:
	docker run -p '9900:9900' local/neru


#########
# mypy

mypy:
	${poetry} run mypy --config-file .mypy.ini .


#########
# black

black:
	${poetry} run black .

black-check:
	${poetry} run black --check .
