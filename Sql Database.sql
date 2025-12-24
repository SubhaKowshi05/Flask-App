-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 02, 2025 at 02:31 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `capstone`
--

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--

CREATE TABLE `comments` (
  `comment_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `comment` varchar(500) NOT NULL,
  `commented_by` varchar(100) NOT NULL,
  `commented_on` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `comments`
--

INSERT INTO `comments` (`comment_id`, `post_id`, `comment`, `commented_by`, `commented_on`) VALUES
(1, 9, 'Wow.. nice dress', 'subha kowshi', '2025-11-09 11:57:12.890266'),
(2, 10, 'My favorite watch also.. Congratulations', 'subha kowshi', '2025-11-09 12:31:03.759983'),
(3, 1, 'i love dogs and your puppy is so cute\r\n', 'subha kowshi', '2025-11-30 15:31:59');

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `contact_id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `description` varchar(800) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contact`
--

INSERT INTO `contact` (`contact_id`, `email`, `description`) VALUES
(1, 'subhakowshi05@gmail.com', 'Hello Capstone! This website is so useful for us..');

-- --------------------------------------------------------

--
-- Table structure for table `friends`
--

CREATE TABLE `friends` (
  `friend_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `requested_id` int(11) NOT NULL,
  `isAccepted` varchar(20) NOT NULL DEFAULT 'False'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `friends`
--

INSERT INTO `friends` (`friend_id`, `user_id`, `requested_id`, `isAccepted`) VALUES
(5, 3, 2, 'False'),
(7, 3, 1, 'False'),
(8, 3, 1, 'True');

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `post_id` int(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `post_title` varchar(100) NOT NULL,
  `post_description` text NOT NULL,
  `image` varchar(500) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp(),
  `time` time NOT NULL,
  `likes` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`post_id`, `email`, `name`, `post_title`, `post_description`, `image`, `date`, `time`, `likes`) VALUES
(1, '', 'Subha Kowshi', 'Dogs', 'Saw acute puppy today', 'wallpaper.jpg', '2025-11-08', '00:00:00', 2),
(2, 'subhakowshi05@gmail.com', 'subha kowshi', 'Watch ', 'My brand new watch', '0-science-and-technology-line-work-summary-plan-powerpoint-background_f11f520bed__960_540.jpg', '2025-11-08', '00:00:00', 1),
(3, 'subhakowshi05@gmail.com', 'subha kowshi', 'My dress', 'Bought a new dress in Zudio yesterday', 'Screenshot_2025-09-11_190214.png', '2025-11-09', '10:43:25', 3),
(4, 'subhakowshi05@gmail.com', 'subha kowshi', 'My watch ', 'Bought a new watch in Titan brand gifted by my friend', 'Screenshot_2025-09-11_192617.png', '2025-11-09', '11:00:34', 3),
(5, 'subhakowshi05@gmail.com', 'subha kowshi', 'Subha', 'rithanya hema', 'Screenshot_2025-09-11_185324.png', '2025-11-09', '12:44:34', 2),
(6, 'yazhini456@gmail.com', 'Yazhini Deva', 'My First Presentation', 'I have done my first presentation for my college', 'Screenshot_2025-05-06_220849.png', '2025-12-01', '13:57:56', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `signup`
--

CREATE TABLE `signup` (
  `user_id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(10) NOT NULL DEFAULT '',
  `password` text NOT NULL,
  `profileimage` varchar(500) NOT NULL DEFAULT 'profile.jpeg'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `signup`
--

INSERT INTO `signup` (`user_id`, `first_name`, `last_name`, `email`, `phone`, `password`, `profileimage`) VALUES
(1, 'Subha', 'Kowshi', 'subhakowshi05@gmail.com', '9360824930', 'scrypt:32768:8:1$U44lJ2H4yGADC0fu$58a78e31d24dc951fd842b82c2ead506e02e23e42a5cde2af565b1d7a3d1e9d611764d88f13e2065f214b5c349d46fa40acd3a7d1365b188bfacb4b0b44ecc03', 'Screenshot_2025-09-11_190214.png'),
(2, 'logi', 'veerasekar', 'logi05@gmail.com', '6379096498', 'scrypt:32768:8:1$OqyWJacKIADPXpa9$23a311d7a47ff156cea3dbe589a5b40195ee17b1c9826245c4c9dee01e97432b7eea85536ad312019ad69aee098e43f4704d5a8332bd694ee1138dd0b9150b31', 'profile.jpg'),
(3, 'Yazhini', 'Deva', 'yazhini456@gmail.com', '9842752588', 'scrypt:32768:8:1$S30Cwcwsh5Dgwkhe$4ee4256b982c12c3815b0cf4ec62b848fccbd073200f1ec8185b28b48c7942369ea0c97ed0fa5e9db9e4fe611e793061393cedf7633efef03c303144451184c6', 'profile.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `socialmedia`
--

CREATE TABLE `socialmedia` (
  `Id` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`comment_id`);

--
-- Indexes for table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`contact_id`);

--
-- Indexes for table `friends`
--
ALTER TABLE `friends`
  ADD PRIMARY KEY (`friend_id`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`post_id`);

--
-- Indexes for table `signup`
--
ALTER TABLE `signup`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `phone` (`phone`);

--
-- Indexes for table `socialmedia`
--
ALTER TABLE `socialmedia`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `comments`
--
ALTER TABLE `comments`
  MODIFY `comment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `contact`
--
ALTER TABLE `contact`
  MODIFY `contact_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `friends`
--
ALTER TABLE `friends`
  MODIFY `friend_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `post_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `signup`
--
ALTER TABLE `signup`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `socialmedia`
--
ALTER TABLE `socialmedia`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
