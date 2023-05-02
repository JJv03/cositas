#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage: $0 <script>"
    exit 85
fi

second_line=$(sed -n 2p "${1}")

#NIP1, last-name1, name1, [MT], [1-5], [AB]
manana_tarde=$(echo "${second_line}" | awk 'BEGIN { FS = "," } ; { print $4 }' | tr -d ' ')
dia=$(echo "${second_line}" | awk 'BEGIN { FS = "," } ; { print $5 }'| tr -d ' ')
tipo_semana=$(echo "${second_line}" | awk 'BEGIN { FS = "," } ; { print $6 }' | tr -d ' ')

grupo="invalido"

if [ "${manana_tarde}" = 'M' ];
then
    grupo="man_"
else
    grupo="tar_"
fi

case $dia in
    1) grupo+="lun_" ;;
    2) grupo+="mar_" ;;
    3) grupo+="mie_" ;;
    4) grupo+="jue_" ;;
    5) grupo+="vie_" ;;
    *) grupo+="XXX_";;
esac

grupo+="${tipo_semana}"

echo "${grupo}"

