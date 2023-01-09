fission spec init
fission env create --spec --name wtc-list-list-env --image x_thebes_answer --poolsize 0 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name wtc-list-list-fn --env wtc-list-list-env --code fission.py --targetcpu 80 --executortype newdeploy --maxscale 3 --requestsperpod 10000 --spec
fission route create --spec --name wtc-list-list-rt --method GET --url /watch_list/list --function wtc-list-list-fn
