CREATE USER 'sersorsProject'@'localhost' IDENTIFIED BY 'sersorsProject';
GRANT ALL PRIVILEGES ON *.* TO 'sersorsProject'@'localhost';
CREATE DATABASE sersorsProject;
USE sersorsProject;
CREATE TABLE temperature(id INT PRIMARY KEY AUTO_INCREMENT,value FLOAT(8,4),timestamp DATETIME,sensor CHAR(255));
CREATE TABLE humidity(id INT PRIMARY KEY AUTO_INCREMENT,value FLOAT(8,4),timestamp DATETIME,sensor CHAR(255));
CREATE TABLE illuminance(id INT PRIMARY KEY AUTO_INCREMENT,value FLOAT(8,4),timestamp DATETIME,sensor CHAR(255));
CREATE TABLE pressure(id INT PRIMARY KEY AUTO_INCREMENT,value FLOAT(8,4),timestamp DATETIME,sensor CHAR(255));
CREATE TABLE noise(id INT PRIMARY KEY AUTO_INCREMENT,value FLOAT(8,4),timestamp DATETIME,sensor CHAR(255));
CREATE TABLE airquality(id INT PRIMARY KEY AUTO_INCREMENT,value FLOAT(8,4),timestamp DATETIME,sensor CHAR(255));