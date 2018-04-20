#!/bin/bash

export FLASK_APP=eftversion/app.py
export FLASK_DEBUG=true
flask $@
