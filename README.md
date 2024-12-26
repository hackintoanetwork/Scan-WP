# Wordpress Plugin Scanner
HackingCamp 27, PoC Security ( CTF Player to Hacker : 선택과 집중 )

# Setting up WordPress with Docker

## Basic WordPress Docker Setup
```bash
# 1. Pull required images
docker pull mysql:5.7
docker pull wordpress

# 2. Create MySQL container
docker run -d --name mysql_db \
  -e MYSQL_ROOT_PASSWORD=toor \
  -e MYSQL_DATABASE=wpdb \
  -e MYSQL_USER=wp \
  -e MYSQL_PASSWORD=wppass \
  -v mysql:/var/lib/mysql \
  mysql:5.7

# 3. Create WordPress container
docker run -d --name wp \
  -p 8080:80 \
  --link mysql_db:wpdb \
  -e WORDPRESS_DB_HOST=wpdb \
  -e WORDPRESS_DB_USER=wp \
  -e WORDPRESS_DB_PASSWORD=wppass \
  -e WORDPRESS_DB_NAME=wpdb \
  -v wp:/var/www/html \
  wordpress
```

## One-Line Command (Apple Silicon/M1/M2)
```bash
docker pull mysql:5.7 --platform linux/amd64; \
docker pull wordpress --platform linux/amd64; \
docker run -d --name mysql_db \
  -e MYSQL_ROOT_PASSWORD=toor \
  -e MYSQL_DATABASE=wpdb \
  -e MYSQL_USER=wp \
  -e MYSQL_PASSWORD=wppass \
  -v mysql:/var/lib/mysql mysql:5.7; \
docker run -d --name wp \
  -p 8888:80 \
  --link mysql_db:wpdb \
  -e WORDPRESS_DB_HOST=wpdb \
  -e WORDPRESS_DB_USER=wp \
  -e WORDPRESS_DB_PASSWORD=wppass \
  -e WORDPRESS_DB_NAME=wpdb \
  -v wp:/var/www/html wordpress
```

**Note:**
- External Port: 8888
- Internal Port: 80
- MySQL Password: wppass

## Accessing Container Shells
```bash
# Access WordPress container
docker exec -it wp bash

# Access MySQL container
docker exec -it mysql_db bash
```

## Accessing MySQL in Container
```bash
# 1. First access the MySQL container
docker exec -it mysql_db bash

# 2. Then connect to MySQL
mysql -u wp -p
# Enter password when prompted: wppass

# 3. Basic MySQL commands
mysql> show databases;
# Should display 'wpdb' and 'information_schema'

# 4. Exit MySQL and container
mysql> exit
root@container:/# exit
```

# Wordpress Docker Setup
![img](https://raw.githubusercontent.com/hackintoanetwork/Scan-WP/main/png/01.png)
![img](https://raw.githubusercontent.com/hackintoanetwork/Scan-WP/main/png/02.png)
![img](https://raw.githubusercontent.com/hackintoanetwork/Scan-WP/main/png/03.png)
![img](https://raw.githubusercontent.com/hackintoanetwork/Scan-WP/main/png/04.png)
![img](https://raw.githubusercontent.com/hackintoanetwork/Scan-WP/main/png/05.png)
![img](https://raw.githubusercontent.com/hackintoanetwork/Scan-WP/main/png/06.png)
