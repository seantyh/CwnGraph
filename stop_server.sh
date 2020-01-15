#!/bin/bash

kill -9 $(cat run_server_CwnServer.pid)
kill -9 $(cat run_server_CwnEdit.pid)
rm -f run_server_CwnServer.pid
rm -f run_server_CwnEdit.pid