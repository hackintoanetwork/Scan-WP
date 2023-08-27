# Scan-WP
Wordpress Plugin Vulnerability Scanner by hackintoanetwork
```
Docker wordpress 구축

1. docker pull mysql:5.7

2. docker pull wordpress

3. docker run -d --name mysql_db -e MYSQL_ROOT_PASSWORD=toor -e MYSQL_DATABASE=wpdb -e MYSQL_USER=wp -e MYSQL_PASSWORD=wppass -v mysql:/var/lib/mysql mysql:5.7

4. docker run -d --name wp -p 8080:80 --link mysql_db:wpdb -e WORDPRESS_DB_HOST=wpdb -e WORDPRESS_DB_USER=wp -e WORDPRESS_DB_PASSWORD=wppass -e WORDPRESS_DB_NAME=wpdb -v wp:/var/www/html wordpress

One Line Command

* docker pull mysql:5.7 --platform linux/amd64; docker pull wordpress --platform linux/amd64; docker run -d --name mysql_db -e MYSQL_ROOT_PASSWORD=toor -e MYSQL_DATABASE=wpdb -e MYSQL_USER=wp -e MYSQL_PASSWORD=wppass -v mysql:/var/lib/mysql mysql:5.7; docker run -d --name wp -p 8888:80 --link mysql_db:wpdb -e WORDPRESS_DB_HOST=wpdb -e WORDPRESS_DB_USER=wp -e WORDPRESS_DB_PASSWORD=wppass -e WORDPRESS_DB_NAME=wpdb -v wp:/var/www/html wordpress

PORT : 내부 포트는 80 이고 외부 포트는 8888 (외부에선 8888으로 들어가야 함)
MYSQL PASSWORD : wppass

Docker 초기화

1. docker stop $(docker ps -a -q)

2. docker rm $(docker ps -a -q)

3. docker rmi $(docker images -q)

4. docker volume prune

One Line Command

* docker stop $(docker ps -a -q); docker rm $(docker ps -a -q); docker rmi $(docker images -q); docker volume prune
```
