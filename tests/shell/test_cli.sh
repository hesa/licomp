#!/bin/bash

# SPDX-FileCopyrightText: 2021 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

dummy_cli()
{
    PYTHONPATH=. python3 tests/python/dummy_main.py $*
}

check_resp()
{
    ACTUAL="$1"
    EXPECTED="$2"

    if [ "$ACTUAL" != "$EXPECTED" ]
    then
        echo "\"$ACTUAL\" != \"$EXPECTED\" :(" 
        exit 1
    fi
}

run_comp_test()
{
    EXP=$1
    shift
    RESP=$(dummy_cli $* | jq -r .compatibility_status)
    printf "%-75s" "$*: "
    check_resp $RESP $EXP
    echo "OK"
}

run_list_test()
{
    EXP=$1
    shift
    RESP=$(dummy_cli $* | jq -r .[] | wc -l)
    printf "%-75s" "$*: "
    check_resp $RESP $EXP
    echo "OK"
}


run_fail_test()
{
    EXP=$1
    shift
    FAILURE=$(dummy_cli $* 2>&1 | jq -r .status)
    if [ "$FAILURE" != "failure" ]
    then
	echo "No expected failure on $*"
	exit 1
    fi
    RESP=$(dummy_cli $* 2>&1 | jq -r .message)
    printf "%-75s" "$*: "
    check_resp "$RESP" "$EXP"
    echo "OK"
}

run_comp_test "yes" "verify -il BSD-3-Clause -ol GPL-2.0-only"
run_comp_test "no" "verify -il GPL-2.0-only -ol BSD-3-Clause"

run_comp_test "null" "verify -il GPL-2.0-only -ol DO_NOT_EXIST"
run_comp_test "null" "verify -il DO_NOT_EXIST -ol BSD-3-Clause"
run_comp_test "null" "verify -il DO_NOT_EXIST -ol DO_NOT_EXIST"

run_comp_test "null" "verify -il GPL-2.0-only -ol DO_NOT_EXIST"
run_comp_test "null" "verify -il DO_NOT_EXIST -ol BSD-3-Clause"
run_comp_test "null" "verify -il DO_NOT_EXIST -ol DO_NOT_EXIST"

run_fail_test "Usecase nonesuch not supported." " -u nonesuch verify -il DO_NOT_EXIST -ol DO_NOT_EXIST"
run_fail_test "Provisioning nonesuch not supported." " -p nonesuch verify -il DO_NOT_EXIST -ol DO_NOT_EXIST"

run_list_test 3 supported-licenses
run_list_test 1 supported-provisionings
run_list_test 1 supported-usecases
