/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.5.29-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: tango
-- ------------------------------------------------------
-- Server version	10.5.29-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `access_address`
--

DROP TABLE IF EXISTS `access_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `access_address` (
  `user` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `netmask` varchar(255) DEFAULT 'FF.FF.FF.FF',
  `updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `accessed` timestamp NOT NULL DEFAULT '1999-12-31 23:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `access_address`
--

LOCK TABLES `access_address` WRITE;
/*!40000 ALTER TABLE `access_address` DISABLE KEYS */;
/*!40000 ALTER TABLE `access_address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `access_device`
--

DROP TABLE IF EXISTS `access_device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `access_device` (
  `user` varchar(255) DEFAULT NULL,
  `device` varchar(255) DEFAULT NULL,
  `rights` varchar(255) DEFAULT NULL,
  `updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `accessed` timestamp NOT NULL DEFAULT '1999-12-31 23:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `access_device`
--

LOCK TABLES `access_device` WRITE;
/*!40000 ALTER TABLE `access_device` DISABLE KEYS */;
/*!40000 ALTER TABLE `access_device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attribute_alias`
--

DROP TABLE IF EXISTS `attribute_alias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `attribute_alias` (
  `alias` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `device` varchar(255) NOT NULL DEFAULT '',
  `attribute` varchar(255) NOT NULL DEFAULT '',
  `updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `accessed` timestamp NOT NULL DEFAULT '1999-12-31 23:00:00',
  `comment` text DEFAULT NULL,
  KEY `index_attribute_alias` (`alias`(64),`name`(64))
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attribute_alias`
--

LOCK TABLES `attribute_alias` WRITE;
/*!40000 ALTER TABLE `attribute_alias` DISABLE KEYS */;
/*!40000 ALTER TABLE `attribute_alias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attribute_class`
--

DROP TABLE IF EXISTS `attribute_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `attribute_class` (
  `class` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `accessed` timestamp NOT NULL DEFAULT '1999-12-31 23:00:00',
  `comment` text DEFAULT NULL,
  KEY `index_attribute_class` (`class`(64),`name`(64))
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attribute_class`
--

LOCK TABLES `attribute_class` WRITE;
/*!40000 ALTER TABLE `attribute_class` DISABLE KEYS */;
/*!40000 ALTER TABLE `attribute_class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_attribute_history_id`
--

DROP TABLE IF EXISTS `class_attribute_history_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_attribute_history_id` (
  `id` bigint(20) unsigned NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_attribute_history_id`
--

LOCK TABLES `class_attribute_history_id` WRITE;
/*!40000 ALTER TABLE `class_attribute_history_id` DISABLE KEYS */;
INSERT INTO `class_attribute_history_id` VALUES (0);
/*!40000 ALTER TABLE `class_attribute_history_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_history_id`
--

DROP TABLE IF EXISTS `class_history_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_history_id` (
  `id` bigint(20) unsigned NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_history_id`
--

LOCK TABLES `class_history_id` WRITE;
/*!40000 ALTER TABLE `class_history_id` DISABLE KEYS */;
INSERT INTO `class_history_id` VALUES (0);
/*!40000 ALTER TABLE `class_history_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_pipe_history_id`
--

DROP TABLE IF EXISTS `class_pipe_history_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_pipe_history_id` (
  `id` bigint(20) unsigned NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_pipe_history_id`
--

LOCK TABLES `class_pipe_history_id` WRITE;
/*!40000 ALTER TABLE `class_pipe_history_id` DISABLE KEYS */;
INSERT INTO `class_pipe_history_id` VALUES (0);
/*!40000 ALTER TABLE `class_pipe_history_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `device` (
  `name` varchar(255) NOT NULL DEFAULT 'nada',
  `alias` varchar(255) DEFAULT NULL,
  `domain` varchar(85) NOT NULL DEFAULT 'nada',
  `family` varchar(85) NOT NULL DEFAULT 'nada',
  `member` varchar(85) NOT NULL DEFAULT 'nada',
  `exported` int(11) DEFAULT 0,
  `ior` text DEFAULT NULL,
  `host` varchar(255) NOT NULL DEFAULT 'nada',
  `server` varchar(255) NOT NULL DEFAULT 'nada',
  `pid` int(11) DEFAULT 0,
  `class` varchar(255) NOT NULL DEFAULT 'nada',
  `version` varchar(8) NOT NULL DEFAULT 'nada',
  `started` datetime DEFAULT NULL,
  `stopped` datetime DEFAULT NULL,
  `comment` text DEFAULT NULL,
  KEY `name` (`name`(64),`alias`(64))
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
INSERT INTO `device` VALUES ('dserver/databaseds/2',NULL,'dserver','databaseds','2',1,'IOR:010000001700000049444c3a54616e676f2f4465766963655f353a312e3000000100000000000000b8000000010102000f0000003132382e3134312e38302e32343500001027000014000000647365727665722f646174616261736564732f320300000000000000080000000100000000545441010000001c00000001000000010001000100000001000105090101000100000009010100025454414400000001000000120000006e61363264637339392e6365726e2e6368000000240000002f746d702f6f6d6e692d726f6f742f3030303030313431342d3137373938373332383000','na62dcs99.cern.ch','Databaseds/2',1414,'DServer','5','2026-05-27 11:14:41','2026-05-22 17:03:38',NULL),('sys/database/2',NULL,'sys','database','2',1,'IOR:010000001700000049444c3a54616e676f2f4465766963655f353a312e3000000100000000000000ac000000010102000f0000003132382e3134312e38302e3234350000102700000800000064617461626173650300000000000000080000000100000000545441010000001c00000001000000010001000100000001000105090101000100000009010100025454414400000001000000120000006e61363264637339392e6365726e2e6368000000240000002f746d702f6f6d6e692d726f6f742f3030303030313431342d3137373938373332383000','na62dcs99.cern.ch','Databaseds/2',1414,'Database','5','2026-05-27 11:14:41','2026-05-22 17:03:38',NULL),('spd/caensmarthv/strawtrackercaenhv_0',NULL,'spd','caensmarthv','strawtrackercaenhv_0',1,'IOR:010000001700000049444c3a54616e676f2f4465766963655f363a312e3000000100000000000000e2000000010102000f0000003132382e3134312e38302e3234350000598500000e000000fe3cb6166a00000771000000000000000400000000000000080000000100000000545441010000001c0000000100000001000100010000000100010509010100010000000901010003000000240000000100000019000000323030313a313435383a3230323a66663a3a3130303a313600005985025454414600000001000000120000006e61363264637339392e6365726e2e6368000000260000002f746d702f6f6d6e692d7370646463732f3030303030313930352d3137373938373333343000','na62dcs99.cern.ch','CaenSMARTHV/StrawTrackerCaenHV_0',1905,'CaenSMARTHV','6','2026-05-27 11:15:40',NULL,NULL),('spd/strawtracker/caensmart01',NULL,'spd','strawtracker','caensmart01',1,'IOR:010000001700000049444c3a54616e676f2f4465766963655f363a312e3000000100000000000000e2000000010102000f0000003132382e3134312e38302e3234350000598500000e000000fe3cb6166a00000771000000000100000400000000000000080000000100000000545441010000001c0000000100000001000100010000000100010509010100010000000901010003000000240000000100000019000000323030313a313435383a3230323a66663a3a3130303a313600005985025454414600000001000000120000006e61363264637339392e6365726e2e6368000000260000002f746d702f6f6d6e692d7370646463732f3030303030313930352d3137373938373333343000','na62dcs99.cern.ch','CaenSMARTHV/StrawTrackerCaenHV_0',1905,'CaenSMARTHV','6','2026-05-27 11:15:40',NULL,NULL),('dserver/CaenSMARTHV/StrawTrackerCaenHV_0',NULL,'dserver','CaenSMARTHV','StrawTrackerCaenHV_0',1,'IOR:010000001700000049444c3a54616e676f2f4465766963655f363a312e3000000100000000000000e2000000010102000f0000003132382e3134312e38302e3234350000598500000e000000fe3cb6166a00000771000000000200000400000000000000080000000100000000545441010000001c0000000100000001000100010000000100010509010100010000000901010003000000240000000100000019000000323030313a313435383a3230323a66663a3a3130303a313600005985025454414600000001000000120000006e61363264637339392e6365726e2e6368000000260000002f746d702f6f6d6e692d7370646463732f3030303030313930352d3137373938373333343000','na62dcs99.cern.ch','CaenSMARTHV/StrawTrackerCaenHV_0',1905,'DServer','6','2026-05-27 11:15:40',NULL,NULL);
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_attribute_history_id`
--

DROP TABLE IF EXISTS `device_attribute_history_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `device_attribute_history_id` (
  `id` bigint(20) unsigned NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_attribute_history_id`
--

LOCK TABLES `device_attribute_history_id` WRITE;
/*!40000 ALTER TABLE `device_attribute_history_id` DISABLE KEYS */;
INSERT INTO `device_attribute_history_id` VALUES (0);
/*!40000 ALTER TABLE `device_attribute_history_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_history_id`
--

DROP TABLE IF EXISTS `device_history_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `device_history_id` (
  `id` bigint(20) unsigned NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_history_id`
--

LOCK TABLES `device_history_id` WRITE;
/*!40000 ALTER TABLE `device_history_id` DISABLE KEYS */;
INSERT INTO `device_history_id` VALUES (2);
/*!40000 ALTER TABLE `device_history_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_pipe_history_id`
--

DROP TABLE IF EXISTS `device_pipe_history_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `device_pipe_history_id` (
  `id` bigint(20) unsigned NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_pipe_history_id`
--

LOCK TABLES `device_pipe_history_id` WRITE;
/*!40000 ALTER TABLE `device_pipe_history_id` DISABLE KEYS */;
INSERT INTO `device_pipe_history_id` VALUES (0);
/*!40000 ALTER TABLE `device_pipe_history_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `event` (
  `name` varchar(255) DEFAULT NULL,
  `exported` int(11) DEFAULT NULL,
  `ior` text DEFAULT NULL,
  `host` varchar(255) DEFAULT NULL,
  `server` varchar(255) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  `version` varchar(8) DEFAULT NULL,
  `started` datetime DEFAULT NULL,
  `stopped` datetime DEFAULT NULL,
  KEY `index_name` (`name`(64))
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `object_history_id`
--

DROP TABLE IF EXISTS `object_history_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `object_history_id` (
  `id` bigint(20) unsigned NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `object_history_id`
--

LOCK TABLES `object_history_id` WRITE;
/*!40000 ALTER TABLE `object_history_id` DISABLE KEYS */;
INSERT INTO `object_history_id` VALUES (0);
/*!40000 ALTER TABLE `object_history_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property`
--

DROP TABLE IF EXISTS `property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `property` (
  `object` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  `value` text DEFAULT NULL,
  `updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `accessed` timestamp NOT NULL DEFAULT '1999-12-31 23:00:00',
  `comment` text DEFAULT NULL,
  KEY `index_name` (`object`(64),`name`(64))
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property`
--

LOCK TABLES `property` WRITE;
/*!40000 ALTER TABLE `property` DISABLE KEYS */;
/*!40000 ALTER TABLE `property` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_attribute_class`
--

DROP TABLE IF EXISTS `property_attribute_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_attribute_class` (
  `class` varchar(255) NOT NULL DEFAULT '',
  `attribute` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `count` int(11) NOT NULL DEFAULT 0,
  `value` text DEFAULT NULL,
  `updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `accessed` timestamp NOT NULL DEFAULT '1999-12-31 23:00:00',
  `comment` text DEFAULT NULL,
  KEY `index_property_attribute_class` (`class`(64),`attribute`(64),`name`(64),`count`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_attribute_class`
--

LOCK TABLES `property_attribute_class` WRITE;
/*!40000 ALTER TABLE `property_attribute_class` DISABLE KEYS */;
/*!40000 ALTER TABLE `property_attribute_class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_attribute_class_hist`
--

DROP TABLE IF EXISTS `property_attribute_class_hist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_attribute_class_hist` (
  `id` bigint(20) unsigned NOT NULL DEFAULT 0,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `class` varchar(255) NOT NULL DEFAULT '',
  `attribute` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `count` int(11) NOT NULL DEFAULT 0,
  `value` text DEFAULT NULL,
  PRIMARY KEY (`id`,`count`),
  KEY `class_attribute_name` (`class`,`attribute`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_attribute_class_hist`
--

LOCK TABLES `property_attribute_class_hist` WRITE;
/*!40000 ALTER TABLE `property_attribute_class_hist` DISABLE KEYS */;
/*!40000 ALTER TABLE `property_attribute_class_hist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_attribute_device`
--

DROP TABLE IF EXISTS `property_attribute_device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_attribute_device` (
  `device` varchar(255) NOT NULL DEFAULT '',
  `attribute` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `count` int(11) NOT NULL DEFAULT 0,
  `value` text DEFAULT NULL,
  `updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `accessed` timestamp NOT NULL DEFAULT '1999-12-31 23:00:00',
  `comment` text DEFAULT NULL,
  KEY `index_property_attribute_device` (`device`(64),`attribute`(64),`name`(64),`count`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_attribute_device`
--

LOCK TABLES `property_attribute_device` WRITE;
/*!40000 ALTER TABLE `property_attribute_device` DISABLE KEYS */;
/*!40000 ALTER TABLE `property_attribute_device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_attribute_device_hist`
--

DROP TABLE IF EXISTS `property_attribute_device_hist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_attribute_device_hist` (
  `id` bigint(20) unsigned NOT NULL DEFAULT 0,
  `count` int(11) NOT NULL DEFAULT 0,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `device` varchar(255) NOT NULL DEFAULT '',
  `attribute` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `value` text DEFAULT NULL,
  PRIMARY KEY (`id`,`count`),
  KEY `device_attribute_name` (`device`,`attribute`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_attribute_device_hist`
--

LOCK TABLES `property_attribute_device_hist` WRITE;
/*!40000 ALTER TABLE `property_attribute_device_hist` DISABLE KEYS */;
/*!40000 ALTER TABLE `property_attribute_device_hist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_class`
--

DROP TABLE IF EXISTS `property_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_class` (
  `class` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `count` int(11) NOT NULL DEFAULT 0,
  `value` text DEFAULT NULL,
  `updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `accessed` timestamp NOT NULL DEFAULT '1999-12-31 23:00:00',
  `comment` text DEFAULT NULL,
  KEY `index_property` (`class`(64),`name`(64),`count`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_class`
--

LOCK TABLES `property_class` WRITE;
/*!40000 ALTER TABLE `property_class` DISABLE KEYS */;
/*!40000 ALTER TABLE `property_class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_class_hist`
--

DROP TABLE IF EXISTS `property_class_hist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_class_hist` (
  `id` bigint(20) unsigned NOT NULL DEFAULT 0,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `class` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `count` int(11) NOT NULL DEFAULT 0,
  `value` text DEFAULT NULL,
  PRIMARY KEY (`id`,`count`),
  KEY `class_name` (`class`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_class_hist`
--

LOCK TABLES `property_class_hist` WRITE;
/*!40000 ALTER TABLE `property_class_hist` DISABLE KEYS */;
/*!40000 ALTER TABLE `property_class_hist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_device`
--

DROP TABLE IF EXISTS `property_device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_device` (
  `device` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `domain` varchar(255) NOT NULL DEFAULT '',
  `family` varchar(255) NOT NULL DEFAULT '',
  `member` varchar(255) NOT NULL DEFAULT '',
  `count` int(11) NOT NULL DEFAULT 0,
  `value` text DEFAULT NULL,
  `updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `accessed` timestamp NOT NULL DEFAULT '1999-12-31 23:00:00',
  `comment` text DEFAULT NULL,
  KEY `index_resource` (`device`(64),`name`(64),`count`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_device`
--

LOCK TABLES `property_device` WRITE;
/*!40000 ALTER TABLE `property_device` DISABLE KEYS */;
INSERT INTO `property_device` VALUES ('spd/caensmarthv/strawtrackercaenhv_0','OpcUrl','','','',1,'opc.tcp://localhost:4801','2026-05-22 15:04:30','2026-05-22 15:04:30',NULL),('spd/strawtracker/caensmart01','OpcUrl','','','',1,'opc.tcp://localhost:4801','2026-05-22 15:04:30','2026-05-22 15:04:30',NULL);
/*!40000 ALTER TABLE `property_device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_device_hist`
--

DROP TABLE IF EXISTS `property_device_hist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_device_hist` (
  `id` bigint(20) unsigned NOT NULL DEFAULT 0,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `device` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `count` int(11) NOT NULL DEFAULT 0,
  `value` text DEFAULT NULL,
  PRIMARY KEY (`id`,`count`),
  KEY `device_name` (`device`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_device_hist`
--

LOCK TABLES `property_device_hist` WRITE;
/*!40000 ALTER TABLE `property_device_hist` DISABLE KEYS */;
INSERT INTO `property_device_hist` VALUES (1,'2026-05-22 15:04:30','spd/caensmarthv/strawtrackercaenhv_0','OpcUrl',1,'opc.tcp://localhost:4801'),(2,'2026-05-22 15:04:30','spd/strawtracker/caensmart01','OpcUrl',1,'opc.tcp://localhost:4801');
/*!40000 ALTER TABLE `property_device_hist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_hist`
--

DROP TABLE IF EXISTS `property_hist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_hist` (
  `id` bigint(20) unsigned NOT NULL DEFAULT 0,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `object` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `count` int(11) NOT NULL DEFAULT 0,
  `value` text DEFAULT NULL,
  PRIMARY KEY (`id`,`count`),
  KEY `object_name` (`object`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_hist`
--

LOCK TABLES `property_hist` WRITE;
/*!40000 ALTER TABLE `property_hist` DISABLE KEYS */;
/*!40000 ALTER TABLE `property_hist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_pipe_class`
--

DROP TABLE IF EXISTS `property_pipe_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_pipe_class` (
  `class` varchar(255) NOT NULL DEFAULT '',
  `pipe` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `count` int(11) NOT NULL DEFAULT 0,
  `value` text DEFAULT NULL,
  `updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `accessed` timestamp NOT NULL DEFAULT '1999-12-31 23:00:00',
  `comment` text DEFAULT NULL,
  KEY `index_property_pipe_class` (`class`(64),`pipe`(64),`name`(64),`count`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_pipe_class`
--

LOCK TABLES `property_pipe_class` WRITE;
/*!40000 ALTER TABLE `property_pipe_class` DISABLE KEYS */;
/*!40000 ALTER TABLE `property_pipe_class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_pipe_class_hist`
--

DROP TABLE IF EXISTS `property_pipe_class_hist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_pipe_class_hist` (
  `id` bigint(20) unsigned NOT NULL DEFAULT 0,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `class` varchar(255) NOT NULL DEFAULT '',
  `pipe` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `count` int(11) NOT NULL DEFAULT 0,
  `value` text DEFAULT NULL,
  PRIMARY KEY (`id`,`count`),
  KEY `class_pipe_name` (`class`,`pipe`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_pipe_class_hist`
--

LOCK TABLES `property_pipe_class_hist` WRITE;
/*!40000 ALTER TABLE `property_pipe_class_hist` DISABLE KEYS */;
/*!40000 ALTER TABLE `property_pipe_class_hist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_pipe_device`
--

DROP TABLE IF EXISTS `property_pipe_device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_pipe_device` (
  `device` varchar(255) NOT NULL DEFAULT '',
  `pipe` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `count` int(11) NOT NULL DEFAULT 0,
  `value` text DEFAULT NULL,
  `updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `accessed` timestamp NOT NULL DEFAULT '1999-12-31 23:00:00',
  `comment` text DEFAULT NULL,
  KEY `index_property_pipe_device` (`device`(64),`pipe`(64),`name`(64),`count`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_pipe_device`
--

LOCK TABLES `property_pipe_device` WRITE;
/*!40000 ALTER TABLE `property_pipe_device` DISABLE KEYS */;
/*!40000 ALTER TABLE `property_pipe_device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_pipe_device_hist`
--

DROP TABLE IF EXISTS `property_pipe_device_hist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_pipe_device_hist` (
  `id` bigint(20) unsigned NOT NULL DEFAULT 0,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `device` varchar(255) NOT NULL DEFAULT '',
  `pipe` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `count` int(11) NOT NULL DEFAULT 0,
  `value` text DEFAULT NULL,
  PRIMARY KEY (`id`,`count`),
  KEY `device_pipe_name` (`device`,`pipe`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_pipe_device_hist`
--

LOCK TABLES `property_pipe_device_hist` WRITE;
/*!40000 ALTER TABLE `property_pipe_device_hist` DISABLE KEYS */;
/*!40000 ALTER TABLE `property_pipe_device_hist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server`
--

DROP TABLE IF EXISTS `server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `server` (
  `name` varchar(255) NOT NULL DEFAULT '',
  `host` varchar(255) NOT NULL DEFAULT '',
  `mode` int(11) DEFAULT 0,
  `level` int(11) DEFAULT 0,
  KEY `index_name` (`name`(64))
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server`
--

LOCK TABLES `server` WRITE;
/*!40000 ALTER TABLE `server` DISABLE KEYS */;
INSERT INTO `server` VALUES ('Databaseds/2','na62dcs99.cern.ch',1,0);
/*!40000 ALTER TABLE `server` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-27 15:56:33
