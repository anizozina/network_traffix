#!/bin/bash -e

local_log_dir="$(pwd)/logs"
remote_log_dir="xxx@192.168.1.20:~/workspace/tcpdumplog/"

# ローカル端末からリモート端末にログファイルを転送、リモートから削除
rsync -av \
  --ignore-errors \
	--ignore-existing \
  --remove-source-files \
  --include="*.pcap" \
  -e "ssh -i ~/.ssh/id_rsa_raspi" \
  "$remote_log_dir" \
  "$local_log_dir" 

python3 main.py
