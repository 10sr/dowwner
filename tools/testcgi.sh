#!/bin/sh

export SERVER_NAME=example.com
export SCRIPT_NAME=./cgi.py
export PATH_INFO=/
export QUERY_STRING=
export REQUEST_METHOD=GET

$SCRIPT_NAME
