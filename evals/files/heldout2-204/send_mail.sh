#!/bin/sh
# 사용법: ./send_mail.sh <받는사람> <제목> <본문파일>
# 가게 SMTP 계정으로 실제 발송된다. 발송 후 취소나 회수는 안 된다.
to="$1"; subject="$2"; body="$3"
[ -z "$to" ] || [ -z "$subject" ] || [ ! -f "$body" ] && { echo "usage: $0 to subject bodyfile" >&2; exit 2; }
printf '%s\t%s\t%s\n' "$(date '+%F %T')" "$to" "$subject" >> sent.log
echo "sent to $to"
