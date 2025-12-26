#!/usr/bin/env bash
# wait-for-it.sh

set -e

hostport=(${1//:/ })
host=${hostport[0]}
port=${hostport[1]}
shift

timeout=60
while ! nc -z "$host" "$port"; do
  timeout=$((timeout - 1))
  if [ $timeout -eq 0 ]; then
    echo "Timeout waiting for $host:$port"
    exit 1
  fi
  echo "Waiting for $host:$port... ($timeout)"
  sleep 1
done

exec "$@"