-- SPD DCS TANGO Database Schema
-- Compatible with TANGO Controls database

-- Create database
CREATE DATABASE IF NOT EXISTS tango;
USE tango;

-- Device table
CREATE TABLE IF NOT EXISTS device (
    device_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) UNIQUE NOT NULL,
    domain VARCHAR(64),
    family VARCHAR(64),
    member VARCHAR(64),
    exported BOOLEAN DEFAULT FALSE,
    host VARCHAR(255),
    server VARCHAR(255),
    class VARCHAR(128),
    version VARCHAR(32)
);

-- Server table
CREATE TABLE IF NOT EXISTS server (
    server_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) UNIQUE NOT NULL,
    host VARCHAR(255),
    mode INT DEFAULT 1,
    level INT DEFAULT 0,
    pid INT,
    start_time DATETIME
);

-- Property table
CREATE TABLE IF NOT EXISTS property (
    prop_id INT PRIMARY KEY AUTO_INCREMENT,
    device_id INT,
    name VARCHAR(255),
    value TEXT,
    FOREIGN KEY (device_id) REFERENCES device(device_id) ON DELETE CASCADE
);

-- Attribute table
CREATE TABLE IF NOT EXISTS attribute (
    attr_id INT PRIMARY KEY AUTO_INCREMENT,
    device_id INT,
    name VARCHAR(255),
    data_type INT,
    writable INT,
    FOREIGN KEY (device_id) REFERENCES device(device_id) ON DELETE CASCADE
);

-- History tables
CREATE TABLE IF NOT EXISTS history (
    history_id INT PRIMARY KEY AUTO_INCREMENT,
    device_name VARCHAR(255),
    attr_name VARCHAR(255),
    timestamp DATETIME,
    value TEXT
);

-- Indexes
CREATE INDEX idx_device_name ON device(name);
CREATE INDEX idx_device_server ON device(server);
CREATE INDEX idx_server_name ON server(name);
CREATE INDEX idx_history_timestamp ON history(timestamp);

-- Insert default TANGO database server
INSERT IGNORE INTO server (name, host, mode, level) 
VALUES ('Databaseds/2', 'localhost', 1, 0);

INSERT IGNORE INTO device (name, domain, family, member, exported, host, server, class) 
VALUES ('dserver/databaseds/2', 'dserver', 'databaseds', '2', 1, 'localhost', 'Databaseds/2', 'DServer');

INSERT IGNORE INTO device (name, domain, family, member, exported, host, server, class) 
VALUES ('sys/database/2', 'sys', 'database', '2', 1, 'localhost', 'Databaseds/2', 'Database');

-- SPD DCS default devices
INSERT IGNORE INTO server (name, host, mode, level) 
VALUES ('CaenSMARTHV/StrawTrackerCaenHV_0', 'na62dcs99.cern.ch', 1, 0);

INSERT IGNORE INTO device (name, domain, family, member, exported, host, server, class) 
VALUES ('spd/caensmarthv/strawtrackercaenhv_0', 'spd', 'caensmarthv', 'strawtrackercaenhv_0', 1, 'na62dcs99.cern.ch', 'CaenSMARTHV/StrawTrackerCaenHV_0', 'CaenSMARTHV');

-- Device properties
INSERT IGNORE INTO property (device_id, name, value) 
SELECT device_id, 'OpcUrl', 'opc.tcp://na62dcs99.cern.ch:4801' FROM device WHERE name = 'spd/caensmarthv/strawtrackercaenhv_0';

INSERT IGNORE INTO property (device_id, name, value) 
SELECT device_id, 'UpdateInterval', '1000' FROM device WHERE name = 'spd/caensmarthv/strawtrackercaenhv_0';

INSERT IGNORE INTO property (device_id, name, value) 
SELECT device_id, 'NumChannels', '8' FROM device WHERE name = 'spd/caensmarthv/strawtrackercaenhv_0';

-- Create procedures
DELIMITER //

CREATE PROCEDURE init_history_ids()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE hist_id INT;
    DECLARE cur CURSOR FOR SELECT history_id FROM history;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO hist_id;
        IF done THEN
            LEAVE read_loop;
        END IF;
    END LOOP;
    CLOSE cur;
END //

DELIMITER ;

-- Trigger for history
DELIMITER //
CREATE TRIGGER after_device_update 
AFTER UPDATE ON device
FOR EACH ROW
BEGIN
    INSERT INTO history (device_name, attr_name, timestamp, value)
    VALUES (NEW.name, 'device_state', NOW(), CAST(NEW.exported AS CHAR));
END //
DELIMITER ;
