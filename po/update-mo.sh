#!/bin/sh

set -eu

. po/gettext-config

Msgfmt () {
	echo msgfmt "$@"
	msgfmt "$@"
}

rm -rf mo

if ! ls po/*.po >/dev/null 2>&1
then
	exit 0
fi

for FILENAME in po/*.po
do
	LANG="$(basename ${FILENAME} .po)"
	DIR="mo/${LANG}/LC_MESSAGES"
	mkdir -p "${DIR}"
	Msgfmt "${FILENAME}" -o "${DIR}/${APPLICATION}.mo"
done
