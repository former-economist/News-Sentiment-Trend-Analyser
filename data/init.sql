CREATE DATABASE IF NOT EXISTS news;
CREATE USER IF NOT EXISTS 'webapp'@'%' IDENTIFIED BY 'b3a5SD31';
GRANT ALL PRIVILEGES ON news.* TO 'webapp'@'%';