#!/bin/bash

#SBATCH -J commet
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -p normal
#SBATCH -t 24:00:00
#SBATCH -A iPlant-Collabs

module load tacc-singularity

set -u

IMG="commet-0.1.0.img"
KMER_SIZE=21
OUT_DIR="$PWD/commet-out"
QUERY=""
QUERY_SET=""

function lc() {
    FILE=$1
    [[ -f "$FILE" ]] && wc -l "$FILE" | cut -d ' ' -f 1
}

function USAGE() {
    printf "Usage:\\n  %s -q QUERY\\n" "$(basename "$0")"
    printf "  %s -Q QUERY_SET\\n\\n" "$(basename "$0")"

    echo "Required arguments:"
    echo " -q QUERY (file or dir, can repeat)"
    echo " or"
    echo " -Q QUERY_SET (Commet query file set)"
    echo ""
    echo "Options:"
    echo " -k KMER_SIZE ($KMER_SIZE)"
    echo " -o OUT_DIR ($OUT_DIR)"
    exit "${1:-0}"
}

[[ $# -eq 0 ]] && USAGE 1

while getopts :k:o:q:Q:h OPT; do
    case $OPT in
        h)
            USAGE
            ;;
        k)
            KMER_SIZE="$OPTARG"
            ;;
        o)
            OUT_DIR="$OPTARG"
            ;;
        q)
            QUERY="$QUERY $OPTARG"
            ;;
        Q)
            QUERY_SET="$OPTARG"
            ;;
        :)
            echo "Error: Option -$OPTARG requires an argument."
            exit 1
            ;;
        \?)
            echo "Error: Invalid option: -${OPTARG:-""}"
            exit 1
    esac
done

if [[ -z "$OUT_DIR" ]]; then
    echo "-o OUT_DIR is required"
    exit 1
fi

if [[ ! -d "$OUT_DIR" ]]; then
    mkdir -p "$OUT_DIR"
fi

if [[ -n "$QUERY" ]]; then
    INPUT_FILES=$(mktemp)
    for QRY in $QUERY; do
        if [[ -f "$QRY" ]]; then
            echo "$QRY" >> "$INPUT_FILES"
        elif [[ -d "$QRY" ]]; then
            find "$QRY" -type f -size +0c | sort >> "$INPUT_FILES"
        else
            echo "\"$QRY\" is neither file nor directory"
        fi
    done

    QUERY_SET="$OUT_DIR/$$.query.set"
    cat /dev/null > "$QUERY_SET"
    i=0
    while read -r FILE; do
        if [[ -f "$FILE" ]]; then
            echo "$(basename $FILE):$FILE" >> "$QUERY_SET"
        else
            echo "FILE \"$FILE\" is not a valid file"
        fi
    done < "$INPUT_FILES"
fi

if [[ -z "$QUERY_SET" ]]; then
    echo "No QUERY_SET"
    exit 1
fi

if [[ ! -f "$QUERY_SET" ]]; then
    echo "QUERY_SET \"$QUERY_SET\" is not a valid file"
    exit 1
fi

echo "Running COMMET"
singularity exec $IMG Commet.py -k "$KMER_SIZE" -o "$OUT_DIR" -b /usr/local/bin "$QUERY_SET"

singularity exec $IMG Commet_analysis.py -o "$OUT_DIR" -b /usr/local/bin "$QUERY_SET"
echo "Done."
echo "Comments to Ken Youens-Clark <kyclark@email.arizona.edu>"
