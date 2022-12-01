-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 01, 2022 at 04:13 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cin_xyz`
--

-- --------------------------------------------------------

--
-- Table structure for table `movies`
--

CREATE TABLE `movies` (
  `id` int(40) NOT NULL,
  `name` varchar(100) NOT NULL,
  `schedule` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `movies`
--

INSERT INTO `movies` (`id`, `name`, `schedule`) VALUES
(1, 'Harry Potter', 'Senin'),
(2, 'Tom and Jerry', 'Senin'),
(3, 'Demon Slayer: Mugen Train', 'Selasa'),
(4, 'Your Name', 'Rabu'),
(5, 'Weathering With You', 'Jumat');

-- --------------------------------------------------------

--
-- Table structure for table `tickets`
--

CREATE TABLE `tickets` (
  `id` int(40) NOT NULL,
  `movie_id` int(11) NOT NULL,
  `schedule` varchar(100) NOT NULL,
  `seat_code` varchar(100) NOT NULL,
  `bought` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tickets`
--

INSERT INTO `tickets` (`id`, `movie_id`, `schedule`, `seat_code`, `bought`) VALUES
(1, 2, 'Senin', '1', 0),
(2, 2, 'Senin', '2', 0),
(3, 2, 'Senin', '3', 0),
(4, 2, 'Senin', '4', 0),
(5, 2, 'Senin', '5', 0),
(6, 3, 'Selasa', '1', 0),
(7, 3, 'Selasa', '2', 0),
(8, 3, 'Selasa', '3', 0),
(9, 3, 'Selasa', '4', 0),
(10, 3, 'Selasa', '5', 0),
(11, 4, 'Rabu', '1', 0),
(12, 4, 'Rabu', '2', 0),
(13, 4, 'Rabu', '3', 0),
(14, 4, 'Rabu', '4', 0),
(15, 4, 'Rabu', '5', 0),
(16, 5, 'Jumat', '1', 0),
(17, 5, 'Jumat', '2', 0),
(18, 5, 'Jumat', '3', 0),
(19, 5, 'Jumat', '4', 0),
(20, 5, 'Jumat', '5', 0),
(21, 0, '1', '1', 0),
(22, 0, '2', '1', 0),
(23, 0, '3', '1', 0),
(24, 0, '4', '1', 0),
(25, 0, '5', '1', 0),
(26, 0, '1', '1', 0),
(27, 0, '2', '1', 0),
(28, 0, '3', '1', 0),
(29, 0, '4', '1', 0),
(30, 0, '5', '1', 0),
(31, 1, 'Senin', '1', 0),
(32, 1, 'Senin', '2', 0),
(33, 1, 'Senin', '3', 0),
(34, 1, 'Senin', '4', 0),
(35, 1, 'Senin', '5', 0);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(40) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `category` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `category`) VALUES
(1, 'darren', '123456', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `movies`
--
ALTER TABLE `movies`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tickets`
--
ALTER TABLE `tickets`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `movies`
--
ALTER TABLE `movies`
  MODIFY `id` int(40) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `tickets`
--
ALTER TABLE `tickets`
  MODIFY `id` int(40) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(40) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
