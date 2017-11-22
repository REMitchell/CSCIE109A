-- phpMyAdmin SQL Dump
-- version 4.7.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 22, 2017 at 05:39 AM
-- Server version: 5.6.35
-- PHP Version: 7.1.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `playlists`
--

-- --------------------------------------------------------

--
-- Table structure for table `artist`
--

CREATE TABLE `artist` (
  `id` int(11) NOT NULL,
  `name` varchar(128) NOT NULL,
  `genres` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(32) NOT NULL,
  `idstr` varchar(28) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`, `idstr`) VALUES
(1, 'Top Lists', 'toplists'),
(2, 'Chill', 'chill'),
(3, 'Mood', 'mood'),
(4, 'Pop', 'pop'),
(5, 'Electronic/Dance', 'edm_dance'),
(6, 'Hip-Hop', 'hiphop'),
(7, 'Party', 'party'),
(8, 'Rock', 'rock'),
(9, 'Workout', 'workout'),
(10, 'Focus', 'focus'),
(11, 'Decades', 'decades'),
(12, 'Dinner', 'dinner'),
(13, 'Sleep', 'sleep'),
(14, 'Indie', 'indie_alt'),
(15, 'R&B', 'rnb'),
(16, 'Trending', 'popculture'),
(17, 'Metal', 'metal'),
(18, 'Soul', 'soul'),
(19, 'Romance', 'romance'),
(20, 'Jazz', 'jazz'),
(21, 'Classical', 'classical'),
(22, 'Latin', 'latin'),
(23, 'Country', 'country'),
(24, 'Folk & Americana', 'folk_americana'),
(25, 'Blues', 'blues'),
(26, 'Travel', 'travel'),
(27, 'Kids', 'kids'),
(28, 'Reggae', 'reggae'),
(29, 'Gaming', 'gaming'),
(30, 'Punk', 'punk'),
(31, 'Funk', 'funk'),
(32, 'Comedy', 'comedy');

-- --------------------------------------------------------

--
-- Table structure for table `playlists`
--

CREATE TABLE `playlists` (
  `id` int(11) NOT NULL,
  `name` varchar(128) NOT NULL,
  `followers` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `songs`
--

CREATE TABLE `songs` (
  `id` int(11) NOT NULL,
  `artistId` int(11) NOT NULL,
  `title` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `artist`
--
ALTER TABLE `artist`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `artist`
--
ALTER TABLE `artist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;