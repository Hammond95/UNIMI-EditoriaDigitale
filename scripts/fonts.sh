#!/bin/bash

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPTDIR"

cat <<'EOT' > /tmp/fontface.def
@font-face {
    font-family: "§NAME§";
    src: url("../fonts/§NAME§.§EXT§");
    font-style: §STYLE§;
    font-weight: §WEIGHT§;
}

EOT

WEIGHTMAP="Bold|bold
Regular|normal
Light|200
Medium|500
SemiBold|600"

STYLEMAP="Normal|normal
Italic|italic
Oblique|oblique"


STDOUT="$1"
if [[ "$STDOUT" == "--stdout" ]]; then
    OUTFILE="/dev/stdout"
else
    OUTFILE="$SCRIPTDIR/../ebook/assets/styles/typography.css"
fi

echo "/* Fonts Definition */" > $OUTFILE

for file in $(ls -1 ../ebook/assets/fonts); do
    filename=$(echo $file | cut -d'.' -f1)
    ext=$(echo $file | cut -d'.' -f2)
    weightkey=$(echo $filename | cut -d'-' -f2)
    stylekey=$(echo $filename | cut -d'-' -f3)

    if [ -z "$weightkey" ]; then
        weight="normal"
    else
        weight=$(echo "$WEIGHTMAP" | grep -E "^$weightkey\|" | cut -d '|' -f2)
    fi

    if [ -z "$stylekey" ]; then
        style="normal"
    else
        style=$(echo "$STYLEMAP" | grep -E "^$stylekey\|"  | cut -d '|' -f2)
    fi

    cat /tmp/fontface.def | sed "s#§NAME§#$filename#g" | sed "s#§EXT§#$ext#g" | sed "s#§WEIGHT§#$weight#g" | sed "s#§STYLE§#$style#g" >> $OUTFILE

done