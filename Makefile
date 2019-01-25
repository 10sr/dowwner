# ENV が local, test でないときは make を使うべきでないかもしれない
DOWWNER_ENV ?= local
DOWWNER_PORT ?= 9900
DOWWNER_HOST ?= 0.0.0.0

ADMIN_USER ?= admin

export DOWWNER_LOCAL_SQLITE3 := $(CURDIR)/db.sqlite3

MAKEFLAGS += --no-builtin-rules --no-builtin-variable

# https://stackoverflow.com/questions/10859916/how-to-treat-a-warning-as-an-error-in-a-makefile/29800774#29800774
MAKECMDGOALS ?= check
# ${MAKECMDGOALS}: fatal-on-warning
fatal-on-warning:
	@! (${MAKE} -n --warn-undefined-variables ${MAKECMDGOALS} 2>&1 >/dev/null | grep 'warning:')


# App label
APP := dowwner

poetry := poetry

python3 := ${poetry} run python3
manage_py := ${python3} ./manage.py
dowwner := ${python3} -m dowwner
env_dowwner := env DOWWNER_ENV=${DOWWNER_ENV}

# Make all targets phony
.PHONY: $(MAKECMDGOALS)

check: poetry-check app-test mypy black-check

env:
	env

################
# Poetry

installdeps:
	${poetry} install

poetry-check:
	${poetry} check

###############
# manage.py

runserver:
	${env_dowwner} ${manage_py} $@ '${DOWWNER_HOST}:${DOWWNER_PORT}'

# https://docs.djangoproject.com/en/1.10/intro/tutorial02/#database-setup
migrate:
	${env_dowwner} ${manage_py} $@

# https://docs.djangoproject.com/en/1.10/intro/tutorial02/#activating-models
makemigrations:
	${env_dowwner} ${manage_py} $@ ${APP}

# Print sql query for migration
sqlmigrate:
	${env_dowwner} ${manage_py} $@ ${APP} ${target}

local_addrecords create_local_user diffsettings:
	${env_dowwner} ${manage_py} $@

shell:
	${env_dowwner} ${manage_py} $@ -i ipython

manage_py:n
	${env_dowwner} ${manage_py} ${command}

app-test:
	env DOWWNER_ENV=test ${manage_py} makemigrations --dry-run --check
	env DOWWNER_ENV=test ${poetry} run coverage run ./manage.py test tests/ --pattern='*.py'

# -m dowwner

add-admin-user:
	${env_dowwner} ${dowwner} $@ ${ADMIN_USER}


###########3
# codecov

codecov:
	${poetry} run codecov


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
