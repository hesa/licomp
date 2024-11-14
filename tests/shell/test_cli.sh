#!/bin/bash

dummy_cli()
{
    PYTHONPATH=. python3 tests/python/dummy_main.py $*
}

check_resp()
{
    ACTUAL=$1
    EXPECTED=$2

    if [ $ACTUAL != $EXPECTED ]
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
    echo -n "$*: "
    check_resp $RESP $EXP
    echo "OK"
}

run_list_test()
{
    EXP=$1
    shift
    RESP=$(dummy_cli $* | jq -r .[] | wc -l)
    echo -n "$*: "
    check_resp $RESP $EXP
    echo "OK"
}



run_comp_test "yes" "verify -il BSD-3-Clause -ol GPL-2.0-only"
run_comp_test "no" "verify -il GPL-2.0-only -ol BSD-3-Clause"

run_comp_test "null" "verify -il GPL-2.0-only -ol DO_NOT_EXIST"
run_comp_test "null" "verify -il DO_NOT_EXIST -ol BSD-3-Clause"
run_comp_test "null" "verify -il DO_NOT_EXIST -ol DO_NOT_EXIST"

run_list_test 2 supported-licenses
run_list_test 1 supported-triggers
