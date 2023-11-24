#!/bin/bash

# validate input args
if [ $# -lt 2 ]; then
	echo "usage: $0 <port> <host>"
	exit 1
fi

port=$1
host=$2

# execute nmap scan + process output
nmap -sT -p "$port" "$host" | grep "/tcp" | awk '{print $1 " " $2}'