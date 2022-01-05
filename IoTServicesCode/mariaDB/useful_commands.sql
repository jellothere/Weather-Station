# create database
create database iot_data;

# Create a new user (only with local access) and grant privileges to this user on the new database:
grant all privileges on iot_data.* TO 'iot_user'@'%' identified by '9R[-RP#64nY7*E*H';

# After modifying the MariaDB grant table, execute the following command in order to apply the changes:
flush privileges;

# create table for sensor data
CREATE TABLE sensor_data (
	id MEDIUMINT NOT NULL AUTO_INCREMENT,
	humidity float NOT NULL,
	temperature float NOT NULL,
    date_time timestamp  NOT NULL,
    device_id varchar(50) NOT NULL,
	PRIMARY KEY (id)
);

# query over table sensor_data
SELECT temperature, humidity FROM sensor_data ORDER BY id DESC LIMIT 1;

# create table for storing device IDs
CREATE TABLE devices (
	device_id varchar(50) NOT NULL,
	status varchar(50) NOT NULL,
	latitude float NOT NULL,
	longitude float NOT NULL,
	date_time timestamp  NOT NULL,
	PRIMARY KEY (device_id)
);

# query over table sensor_data
SELECT device_id FROM devices;
