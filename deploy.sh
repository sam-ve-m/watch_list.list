fission spec init
fission env create --spec --name wtc-list-list-env --image nexus.sigame.com.br/fission-wacth-list-list:0.2.0-2 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name wtc-list-list-fn --env wtc-list-list-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name wtc-list-list-rt --method GET --url /watch_list/list --function wtc-list-list-fn
