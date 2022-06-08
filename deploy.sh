#!/bin/bash
fission spec init
fission env create --spec --name watch-list-list-env --image nexus.sigame.com.br/fission-async:0.1.6 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name watch-list-list-fn --env watch-list-list-env --src "./func/*" --entrypoint main.list_symbols  --rpp 100000
fission route create --spec --method GET --url /watch_list/list --function watch-list-list-fn
