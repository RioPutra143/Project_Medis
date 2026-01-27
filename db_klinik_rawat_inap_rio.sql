-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 13, 2026 at 04:20 AM
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
-- Database: `db_klinik_rawat_inap_rio`
--

-- --------------------------------------------------------

--
-- Table structure for table `kamar_rio`
--

CREATE TABLE `kamar_rio` (
  `id_kamar_rio` varchar(10) NOT NULL,
  `no_kamar_rio` varchar(12) NOT NULL,
  `kelas_rio` varchar(10) NOT NULL,
  `status_kamar_rio` varchar(20) NOT NULL,
  `harga_rio` int(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kamar_rio`
--

INSERT INTO `kamar_rio` (`id_kamar_rio`, `no_kamar_rio`, `kelas_rio`, `status_kamar_rio`, `harga_rio`) VALUES
('K001', '001', 'VVIP', 'Digunakan', 700000),
('K002', '002', 'VIP', 'Digunakan', 500000),
('K003', '003', 'Reguler', 'Digunakan', 200000),
('K004', '004', 'Reguler', 'Digunakan', 200000),
('K005', '005', 'VIP', 'Tersedia', 500000);

-- --------------------------------------------------------

--
-- Table structure for table `pasien_rio`
--

CREATE TABLE `pasien_rio` (
  `id_pasien_rio` varchar(10) NOT NULL,
  `nama_rio` varchar(30) NOT NULL,
  `alamat_rio` varchar(50) NOT NULL,
  `kontak` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pasien_rio`
--

INSERT INTO `pasien_rio` (`id_pasien_rio`, `nama_rio`, `alamat_rio`, `kontak`) VALUES
('P001', 'Rino', 'Bandung', '083827713143'),
('P002', 'Flick', 'Cimahi', '081998298449'),
('P003', 'Zan', 'Baros', '083827713134'),
('P004', 'Verynnn', 'Sunda', '081998298445'),
('P005', 'Menaw', 'Jawa', '083827713343');

-- --------------------------------------------------------

--
-- Table structure for table `rawat_inap_rio`
--

CREATE TABLE `rawat_inap_rio` (
  `id_rawat_rio` varchar(10) NOT NULL,
  `id_pasien_rio` varchar(10) NOT NULL,
  `id_kamar_rio` varchar(10) NOT NULL,
  `tgl_masuk` date NOT NULL,
  `tgl_keluar` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rawat_inap_rio`
--

INSERT INTO `rawat_inap_rio` (`id_rawat_rio`, `id_pasien_rio`, `id_kamar_rio`, `tgl_masuk`, `tgl_keluar`) VALUES
('R001', 'P001', 'K001', '2026-01-13', '2026-01-22'),
('R002', 'P002', 'K002', '2026-01-12', '2026-01-20'),
('R003', 'P003', 'K003', '2026-01-05', '2026-01-14'),
('R004', 'P004', 'K004', '2026-01-13', '2026-01-19'),
('R005', 'P005', 'K005', '0000-00-00', '0000-00-00');

-- --------------------------------------------------------

--
-- Table structure for table `transaksi_rio`
--

CREATE TABLE `transaksi_rio` (
  `id_transaksi` varchar(10) NOT NULL,
  `id_pasien_rio` varchar(10) NOT NULL,
  `total_biaya_rio` int(50) NOT NULL,
  `status_pembayaran_rio` varchar(20) NOT NULL,
  `tgl_transaksi_rio` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_rio`
--

CREATE TABLE `user_rio` (
  `id_user_rio` varchar(10) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_rio`
--

INSERT INTO `user_rio` (`id_user_rio`, `username`, `password`) VALUES
('U001', 'Arvery', '12345'),
('U002', 'Very', '123'),
('U003', 'Dio', '111'),
('U004', 'Zawa', '222'),
('U005', 'Wanda', '777');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `kamar_rio`
--
ALTER TABLE `kamar_rio`
  ADD PRIMARY KEY (`id_kamar_rio`);

--
-- Indexes for table `pasien_rio`
--
ALTER TABLE `pasien_rio`
  ADD PRIMARY KEY (`id_pasien_rio`);

--
-- Indexes for table `rawat_inap_rio`
--
ALTER TABLE `rawat_inap_rio`
  ADD PRIMARY KEY (`id_rawat_rio`),
  ADD KEY `id_pasien_rino` (`id_pasien_rio`),
  ADD KEY `id_kamar_rino` (`id_kamar_rio`);

--
-- Indexes for table `transaksi_rio`
--
ALTER TABLE `transaksi_rio`
  ADD PRIMARY KEY (`id_transaksi`),
  ADD KEY `id_pasien_rio` (`id_pasien_rio`);

--
-- Indexes for table `user_rio`
--
ALTER TABLE `user_rio`
  ADD PRIMARY KEY (`id_user_rio`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `rawat_inap_rio`
--
ALTER TABLE `rawat_inap_rio`
  ADD CONSTRAINT `rawat_inap_rio_ibfk_1` FOREIGN KEY (`id_pasien_rio`) REFERENCES `pasien_rio` (`id_pasien_rio`),
  ADD CONSTRAINT `rawat_inap_rio_ibfk_2` FOREIGN KEY (`id_kamar_rio`) REFERENCES `kamar_rio` (`id_kamar_rio`);

--
-- Constraints for table `transaksi_rio`
--
ALTER TABLE `transaksi_rio`
  ADD CONSTRAINT `transaksi_rio_ibfk_1` FOREIGN KEY (`id_pasien_rio`) REFERENCES `pasien_rio` (`id_pasien_rio`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
