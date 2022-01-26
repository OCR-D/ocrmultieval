#!/bin/bash
TEMPFILE=${TEMPFILE:-/tmp/ocrmultieval-compare-metrics}

backends=(IsriOcreval CorAsvAnnCompare PrimaTextEval ocrevalUAtion dinglehopper)
metrics=(CER WER)
files=(GT.txt DT.txt)

while [[ $1 = -* ]];do
    case $1 in
        --backends) backends=($2); shift ;;
        --metrics) metrics=($2); shift ;;
    esac
    shift
done

if [[ -n $1 ]];then
    files=("$1" "$2")
fi

for backend in "${backends[@]}";do
    scores=$(/usr/bin/time --format="%e %PCPU" -o $TEMPFILE \
        ocrmultieval compare --format yaml $backend "${files[@]}" 2>/dev/null)
    printf "%-20s %s\t" $backend "$(cat $TEMPFILE)"
    for metric in "${metrics[@]}";do
        echo "$scores"|grep -s "$metric:.*"|tr -d '\012\015'
        printf "\t"
    done
    echo
done
