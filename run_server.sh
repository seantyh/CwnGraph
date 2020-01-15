#!/bin/bash
cd /home/seantyh/langon/CwnGraph
nohup /home/seantyh/miniconda3/envs/cwn/bin/gunicorn CwnEdit.server:app \
    --bind 0.0.0.0:5200 \
    -k gthread \
    --workers 1 \
    --threads 4 &> server.nohup.out &
echo $! > run_server_CwnEdit.pid

nohup /home/seantyh/miniconda3/envs/cwn/bin/gunicorn CwnServer.server:app \
    --bind 0.0.0.0:5201 \
    -k gthread \
    --workers 1 \
    --threads 4 &> server.nohup.out &
echo $! > run_server_CwnServer.pid