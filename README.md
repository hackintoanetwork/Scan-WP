# Scan-WP
Wordpress Plugin Vulnerability Scanner by hackintoanetwork
```bash
# Wordpress Docker 구축

1. docker pull mysql:5.7

2. docker pull wordpress

3. docker run -d --name mysql_db -e MYSQL_ROOT_PASSWORD=toor -e MYSQL_DATABASE=wpdb -e MYSQL_USER=wp -e MYSQL_PASSWORD=wppass -v mysql:/var/lib/mysql mysql:5.7

4. docker run -d --name wp -p 8080:80 --link mysql_db:wpdb -e WORDPRESS_DB_HOST=wpdb -e WORDPRESS_DB_USER=wp -e WORDPRESS_DB_PASSWORD=wppass -e WORDPRESS_DB_NAME=wpdb -v wp:/var/www/html wordpress

# One Line Command (Tested on Apple Silicon Mac OSX)

$ docker pull mysql:5.7 --platform linux/amd64; docker pull wordpress --platform linux/amd64; docker run -d --name mysql_db -e MYSQL_ROOT_PASSWORD=toor -e MYSQL_DATABASE=wpdb -e MYSQL_USER=wp -e MYSQL_PASSWORD=wppass -v mysql:/var/lib/mysql mysql:5.7; docker run -d --name wp -p 8888:80 --link mysql_db:wpdb -e WORDPRESS_DB_HOST=wpdb -e WORDPRESS_DB_USER=wp -e WORDPRESS_DB_PASSWORD=wppass -e WORDPRESS_DB_NAME=wpdb -v wp:/var/www/html wordpress

PORT : 내부 포트는 80 이고 외부 포트는 8888 (외부에선 8888으로 들어가야 함)
MYSQL PASSWORD : wppass
```

```bash
# Docker 초기화 (컨테이너 및 이미지 모두 삭제)

1. docker stop $(docker ps -a -q);

2. docker rm $(docker ps -a -q);

3. docker rmi $(docker images -q);

4. docker volume prune;

# One Line Command

$ docker stop $(docker ps -a -q); docker rm $(docker ps -a -q); docker rmi $(docker images -q); docker volume prune
```

```bash
# Docker Container Shell 에 접속

$ docker exec -it wp bash
$ docker exec -it mysql_db bash
```

```bash
# mysql_db Container mysql 접속
root@73ff547924d2:/# mysql -u wp -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 7
Server version: 5.7.34 MySQL Community Server (GPL)

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| wpdb               |
+--------------------+
2 rows in set (0.00 sec)

mysql> exit
Bye
root@73ff547924d2:/# exit
exit
```
