# 1.扫描存活主机，-H 传递“ip，域名，域名文件或ip文件”
python3 scan.py -H 192.168.1.1 ok

python3 scan.py -H 192.168.1.1/24 ok

python3 scan.py -H 192.168.1.1-100 ok

python3 scan.py -H "127.0.0.1 127.0.0.2"

python3 scan.py -H xxx.com ok      

python3 scan.py -H xxx.txt 

# 2.扫描端口-p all 扫描所有端口，-p 80,81,82扫描指定端口, -p 1-1024扫描1到1024端口
python3 scan.py -H 192.168.1.1/24 -p 80 ok

python3 scan.py -H 192.168.1.1/24 -p all ok 

python3 scan.py -H 192.168.1.1-192.168.10.1 -p 80,81,82 ok

python3 scan.py -H xxx.com -p 1-1024 ok      

python3 scan.py -H xxx.txt

# 3.扫描C段
python3 scan.py -H xxx.com -p 80 -C
