SET FOREIGN_KEY_CHECKS=0; 		

DROP TABLE IF EXISTS tac_gia;
CREATE TABLE `tac_gia` (
	`id_tg` 			int NOT NULL AUTO_INCREMENT,
	`ten_tg` 			varchar(50) NOT NULL,
	`email_tg`			varchar(50) NOT NULL,
	`sdt_tg` 			varchar(50) DEFAULT NULL,
	`ns_tg`		 		date DEFAULT NULL,  
	`ten_dn_tg`			varchar(250) NOT NULL,
	`mk_tg`				varchar(250) NOT NULL,    
	PRIMARY KEY (`id_tg`)
);

DROP TABLE IF EXISTS admins;
CREATE TABLE `admins` (
	`id_admin` 			int NOT NULL AUTO_INCREMENT,
	`ten_admin` 		varchar(50) NOT NULL,
	`email_admin`		varchar(50) NOT NULL,
	`sdt_admin`			varchar(50) DEFAULT NULL,
	`ns_admin`	 		date DEFAULT NULL,  
	`ten_dn_admin`		varchar(250) NOT NULL,
	`mk_admin`			varchar(250) NOT NULL,
    `so_bai_duyet`		int,
    `so_bai_go`			int,
	PRIMARY KEY (`id_admin`)
);

DROP TABLE IF EXISTS bai_viet;
CREATE TABLE `bai_viet` (
	`id_bai`			int NOT NULL AUTO_INCREMENT,
    `thoigian_dang`		DATETIME NOT NULL,
    `khu_vuc` 			varchar(50) NOT NULL,    
    `tieu_de`			text,
    `mo_ta`				text,
    `hinh_anh`			LONGBLOB NOT NULL,
    `van_ban`			text,
    `luot_xem`			int,
    `id_ad_duyet`		int,
    `id_ad_go`			int,
    `id_tg`				int,
    `email_dong_tg`		varchar(50),
    `trang_thai`		int,	-- 0: chua duyet,	1: da duyet,	2: da go             
    `thoi_gian_duyet`	DATETIME NOT NULL,
    `thoi_gian_go`		DATETIME NOT NULL,
    `ly_do_go`			text,
    PRIMARY KEY (`id_bai`),
    constraint `fk_baiviet_admin_idadduyet` foreign key (`id_ad_duyet`) references `admins`(`id_admin`),
    constraint `fk_baiviet_admin_idadgo` foreign key (`id_ad_go`) references `admins`(`id_admin`),
    constraint `fk_baiviet_tacgia_idtg` foreign key (`id_tg`) references `tac_gia`(`id_tg`)        
);






