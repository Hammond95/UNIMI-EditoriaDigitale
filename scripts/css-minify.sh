#!/bin/bash

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPTDIR"

cssfiles=("typography.css" "0.css" "1.css" "pgepub.css")

echo "" > /tmp/merged-css.css
for css in "${cssfiles[@]}"; do
    cat "$SCRIPTDIR/../ebook/assets/styles/$css" >> /tmp/merged-css.css
done

curl -X POST -s --data-urlencode "input@/tmp/merged-css.css" https://www.toptal.com/developers/cssminifier/raw > "$SCRIPTDIR/../ebook/assets/styles/minified/style-min.css"