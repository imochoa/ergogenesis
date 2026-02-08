#!/usr/bin/env bash
set -euxo pipefail

: Make sure directories exist:
# mkdir -p "/home/${USER}/"

: Check permissions for mounted directories
for dir in "." "."; do
    printf "Checking group ownership for %s...\n" "${dir}";
    [[ $(stat -c "%g" "${dir}") -eq 1000 ]] && echo -e "OK!" || echo -e "\033[0;41mOWNER WAS NOT 1000\033[0m"
done

