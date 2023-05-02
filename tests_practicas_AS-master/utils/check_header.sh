#!/bin/bash

function usage {
    echo "$0 <file_to_check.sh>"
    echo "The required header format for the first three lines of the script is:"
    echo "#!/bin/bash"
    echo "#NIP1, last-name1, name1, [MT], [1-5], [AB]"
    echo "#NIP2, last-name2, name2, [MT], [1-5], [AB]"
    echo ""
    echo "The third line is optional, and the arguments are as follows:"
    echo -e "\tNIPx, NIPx: Identification number of each student"
    echo -e "\tlast-nameX, nameX: Last name and name of each student"
    echo -e "\t[MT]: Morning or afTernoon of the group"
    echo -e "\t[1-7]: Day of the week for the group. Weeks start with Monday on day 1"
    echo -e "\t[AB]: Week of the group, either A or B"
    echo "Please watch out with extra spaces between the fields"
    echo ""
    echo "Valid header examples:"
    echo -e "\t2 students:"
    echo -e "\t\t#!/bin/bash"
    echo -e "\t\t#214748, Galindo, Beatriz, T, 2, A"
    echo -e "\t\t#429496, Wilkes, Maurice, T, 2, A"
    echo ""
    echo -e "\tSingle student (please note the empty line):"
    echo -e "\t\t#!/bin/bash"
    echo -e "\t\t#214748, Galindo, Beatriz, T, 2, A"
    echo -e "\n"
    echo -e "Error: $@\n\n"
    echo "For comments or suggestions please contact dario@unizar.es"

    exit 85
}

function check_user_line {
    local line="$1"

    echo "${line}" | grep -q '#[0-9]\{6\}, [ñA-Za-z][ñA-Za-z ]*, [ñA-Za-z][ñA-Za-z ]*, [MT], [1-5], [AB]'
    echo "$?"
}

fname="$1"

if [ $# -ne 1 ] || [ "${#fname}" -lt 4 ] || [ ! -r "${fname}" ] || [ "${fname: -3}" != ".sh" ]
then
    usage "Invalid number of script arguments, lines or extension"
fi

# check number of lines
nlines=$(wc -l "$fname" | awk ' { print $1 } ')
[ ${nlines} -ge 3 ] || usage


# check shebang
first_line=$(head -1 "${fname}")
[ "${first_line}" == "#!/bin/bash" ] || usage "Invalid first line: ${first_line}"

# check second line
second_line=$(sed -n 2p "${fname}")
second_line_valid=$(check_user_line "$second_line")
[ "${second_line_valid}" -eq "0" ] || usage "Invalid second line: ${second_line}"

# check third line
third_line=$(sed -n 3p "${fname}")
third_line_valid=$(check_user_line "$third_line")
[ "x${third_line}" == "x" -o "${third_line_valid}" -eq "0" ] || usage "Invalid third line: ${third_line}"

echo "The header is valid"
exit 0
