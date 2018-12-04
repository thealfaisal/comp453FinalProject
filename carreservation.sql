-- phpMyAdmin SQL Dump
-- version 4.8.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 05, 2018 at 12:53 AM
-- Server version: 10.1.34-MariaDB
-- PHP Version: 7.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `carreservation`
--

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer` (
  `customerID` int(11) NOT NULL,
  `username` varchar(30) NOT NULL,
  `firstName` varchar(30) DEFAULT NULL,
  `middleName` varchar(30) DEFAULT NULL,
  `lastName` varchar(30) DEFAULT NULL,
  `email` varchar(30) NOT NULL,
  `password` varchar(100) NOT NULL,
  `phoneNumber` varchar(30) DEFAULT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `state` varchar(20) DEFAULT NULL,
  `zipcode` varchar(20) DEFAULT NULL,
  `admin` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`customerID`, `username`, `firstName`, `middleName`, `lastName`, `email`, `password`, `phoneNumber`, `Address`, `city`, `state`, `zipcode`, `admin`) VALUES
(100001, 'fly', 'Filli', 'Gov', 'Dan', 'fu@gmail.com', 'rebel', '7736530011', '405 N. Street', 'Chicago', 'IL', '60603', 0),
(100003, 'Zon', 'Xaomi', 'Zen', 'Fifi', 'zoo@gmail.com', 'did', '3126530011', '1205 S. Street', 'NY City', 'NY', '40005', 0),
(100004, 'Bio', 'Amy', 'Con', 'Dov', 'vbv@gmail.com', 'pip', '3126533121', '1100 W. Street', 'Huston', 'TX', '50002', 0);

-- --------------------------------------------------------

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
CREATE TABLE `location` (
  `locationID` int(11) NOT NULL,
  `locationName` varchar(30) NOT NULL,
  `city` varchar(20) DEFAULT NULL,
  `state` varchar(20) DEFAULT NULL,
  `zipcode` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `location`
--

INSERT INTO `location` (`locationID`, `locationName`, `city`, `state`, `zipcode`) VALUES
(101, 'Addison', 'Chicago', 'IL', '60002'),
(102, 'Hyde Park', 'Chicago', 'IL', '60003'),
(103, 'Anderson ville', 'Huston', 'TX', '51003');

-- --------------------------------------------------------

--
-- Table structure for table `reservation`
--

DROP TABLE IF EXISTS `reservation`;
CREATE TABLE `reservation` (
  `customerID` int(11) NOT NULL,
  `vehicleID` int(11) NOT NULL,
  `dateFrom` date DEFAULT NULL,
  `dateTo` date DEFAULT NULL,
  `timeFrom` time DEFAULT NULL,
  `timeTo` time DEFAULT NULL,
  `pickupLocation` varchar(50) DEFAULT NULL,
  `dropoffLocation` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `reservation`
--

INSERT INTO `reservation` (`customerID`, `vehicleID`, `dateFrom`, `dateTo`, `timeFrom`, `timeTo`, `pickupLocation`, `dropoffLocation`) VALUES
(100003, 10002, '2018-12-04', '2018-12-01', '10:30:00', '12:00:00', 'Addison', 'Anderson ville'),
(100001, 10003, '2018-12-05', '2018-12-10', '08:30:00', '04:00:00', 'Hyde Park', 'Addison');

-- --------------------------------------------------------

--
-- Table structure for table `vehicle`
--

DROP TABLE IF EXISTS `vehicle`;
CREATE TABLE `vehicle` (
  `vehicleID` int(11) NOT NULL,
  `vinNumber` varchar(30) DEFAULT NULL,
  `engineNumber` varchar(30) DEFAULT NULL,
  `BrandName` varchar(30) NOT NULL,
  `image` varchar(20) DEFAULT NULL,
  `plateNumber` varchar(20) NOT NULL,
  `ModelName` varchar(30) NOT NULL,
  `Year` int(11) DEFAULT NULL,
  `style` varchar(30) DEFAULT NULL,
  `transmission` varchar(20) DEFAULT NULL,
  `trimLevel` varchar(15) DEFAULT NULL,
  `mpg` int(11) DEFAULT NULL,
  `rate` double DEFAULT NULL,
  `locationID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `vehicle`
--

INSERT INTO `vehicle` (`vehicleID`, `vinNumber`, `engineNumber`, `BrandName`, `image`, `plateNumber`, `ModelName`, `Year`, `style`, `transmission`, `trimLevel`, `mpg`, `rate`, `locationID`) VALUES
(10001, '1C6RR7TT2ES224336', '6U90000BB41202329', 'BMW', 'bmw1.png', 'ZD982370', 'I3', 2017, 'Sedan', 'Automatic', 'SE', 16, 70, 103),
(10002, '1C6RR7TT2ES200336', '1U90880BB41202329', 'TOYOTA', 'toyota1.png', 'ZD901256', 'Corolla', 2016, 'Sedan', 'Automatic', 'LE', 29, 72, 102),
(10003, '1C6RR7CC2ES200336', '1U90880BB41808329', 'HONDA', 'honda1.png', 'ZI037816', 'Civic', 2017, 'Sedan', 'Automatic', 'LX', 25, 69, 101);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`customerID`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `location`
--
ALTER TABLE `location`
  ADD PRIMARY KEY (`locationID`);

--
-- Indexes for table `reservation`
--
ALTER TABLE `reservation`
  ADD PRIMARY KEY (`vehicleID`,`customerID`),
  ADD KEY `CustReserv_FK1` (`customerID`);

--
-- Indexes for table `vehicle`
--
ALTER TABLE `vehicle`
  ADD PRIMARY KEY (`vehicleID`),
  ADD KEY `Loc_FK1` (`locationID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `customerID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100005;

--
-- AUTO_INCREMENT for table `location`
--
ALTER TABLE `location`
  MODIFY `locationID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=104;

--
-- AUTO_INCREMENT for table `vehicle`
--
ALTER TABLE `vehicle`
  MODIFY `vehicleID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10004;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `reservation`
--
ALTER TABLE `reservation`
  ADD CONSTRAINT `CustReserv_FK1` FOREIGN KEY (`customerID`) REFERENCES `customer` (`customerID`),
  ADD CONSTRAINT `VehReserv_FK1` FOREIGN KEY (`vehicleID`) REFERENCES `vehicle` (`vehicleID`);

--
-- Constraints for table `vehicle`
--
ALTER TABLE `vehicle`
  ADD CONSTRAINT `Loc_FK1` FOREIGN KEY (`locationID`) REFERENCES `location` (`locationID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
