#!/bin/bash

function log(){
    local level="$1"
    local msg="$2"

    echo -e "$(date +'%Y-%m-%D %H:%M:%S,000') $level\t#0\t$msg"
}

function info(){
    local msg="$1"
    log "INFO" "$msg"
}

function warn(){
    local msg="$1"
    log "WARNING" "$msg"
}

function error(){
    local msg="$1"
    log "ERROR" "$msg"
    exit 1
}

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPTDIR"

info "Running Build Script..."
info "Generating Fonts Definitions (font-face in typography.css)."
. fonts.sh

info "Updating HTML files based on template."
python3 ./update_template.py

info "Generating minified css."
. css-minify.sh

cd $SCRIPTDIR/..
info "Building Ebook with ebookmaker."
pipenv run build-epub