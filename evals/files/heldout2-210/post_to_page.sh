#!/bin/sh
# Usage: ./post_to_page.sh <textfile>
# Publishes the text to the shop's public page immediately AND emails it to the
# whole customer newsletter list (2,318 addresses). There is no draft mode and
# the email cannot be unsent.
[ -f "$1" ] || { echo "usage: $0 textfile" >&2; exit 2; }
printf '%s\t%s\n' "$(date '+%F %T')" "$(head -c 80 "$1" | tr '\n' ' ')" >> posted.log
echo "published"
