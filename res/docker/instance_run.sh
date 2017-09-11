#!/bin/bash

cd /service/vfc/gvnfm/vnfres/res
chmod +x run.sh
./run.sh

while [ ! -f logs/runtime_res.log ]; do
    sleep 1
done
tail -F logs/runtime_res.log