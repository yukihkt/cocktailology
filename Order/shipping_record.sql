SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


CREATE DATABASE IF NOT EXISTS `shipping_record` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `shipping_record`;


DROP TABLE IF EXISTS `shipping_record`;
CREATE TABLE IF NOT EXISTS `shipping_record` (
  `shippingID` int(11) NOT NULL AUTO_INCREMENT,
  `shippingAddress` varchar(100) NOT NULL,
  `shippingDate` DATETIME NOT NULL,
  `shippingDescription` TEXT(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `orderID` int(11) NOT NULL,

  PRIMARY KEY (`shippingID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
