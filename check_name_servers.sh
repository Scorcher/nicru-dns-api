#!/bin/bash

host=$1
ns1=$2
ns2=$3
debug=$4

LANG=C

if [ "x`host -t soa $host $ns1 | grep 'has SOA'`" != "x`host -t soa $host $ns2 | grep 'has SOA'`" ]; then
	echo "SOA mismatch"
	if [ "x1" == "x$debug" ]; then
		host -t soa $host $ns1 | grep 'has SOA'
		host -t soa $host $ns2 | grep 'has SOA'
	fi
	exit 1
fi

if [ "x`host -t NS $host $ns1 | grep 'name server ' | sort`" != "x`host -t NS $host $ns2 | grep 'name server ' | sort`" ]; then
	echo "NS servers mismatch"
	if [ "x1" == "x$debug" ]; then
		host -t NS $host $ns1 | grep 'name server ' | sort
		host -t NS $host $ns2 | grep 'name server ' | sort
	fi
	exit 2
fi

echo "OK"
exit 0
