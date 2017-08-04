#!/bin/bash

if [ -z "$1" ]
  then
    MESSAGE=Hi!
  else
    MESSAGE=$1
fi
if [ -z "$2" ]
  then
    N='1'
  else
    N=$2
fi

echo Send $MESSAGE $N Times
for i in `seq 1 $N`; do
    curl -X POST -H 'Content-type: application/json' --data '{"token": "Qw671KoWqDm3iv2ok3leR9Ko", "team_id": "T03G61VPV", "api_app_id": "A69BQ5S2Z", "event": {"type": "message", "user": "USLACKBOT", "text": "'$MESSAGE'", "ts": "1500183396.097119", "channel": "D03GALK0C", "event_ts": "1500183396.097119"}, "type": "event_callback", "authed_users": ["U03GALK02"], "event_id": "Ev69GLSSGM", "event_time": 1500183396}' http://0.0.0.0:5000/webhook
done
