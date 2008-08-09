#!/bin/sh

set -eu

. po/gettext-config

if [ ! -d po/ ] && [ -d ../po/ ]
then
	cd ..
fi

FILES="$(mktemp)"
trap 'rm -f ${FILES}' EXIT

find ${DIRS} -type f -printf "%p\n" > ${FILES}

REGEX="$(echo ${EXTENSIONS} | sed 's@ @\\|@g')"
sed -i -n -e '/\('"${REGEX}"'\)$/p' ${FILES}

exec xgettext \
	--files-from=${FILES} \
	--default-domain=${APPLICATION} \
	--force-po \
	--foreign-user \
	--package-name=${APPLICATION} \
	--msgid-bugs-address=${EMAIL} \
	--output=po/${APPLICATION}.pot
