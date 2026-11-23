#!/usr/bin/env bash
while true; do printf 'MoSec UDP 9999\n' | nc -u -l -p 9999 -w 1; done
