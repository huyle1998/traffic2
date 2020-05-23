DROP TABLE IF EXISTS admins;
CREATE TABLE `admins` (
	`admin_id` 			int NOT NULL AUTO_INCREMENT,
	`ten_admin` 		varchar(50) NOT NULL,
	`email_admin`		varchar(50) NOT NULL,
	`sdt` 				varchar(50) DEFAULT NULL,
	`ngay_sinh` 		date DEFAULT NULL,  
	`ten_dang_nhap`		varchar(50) NOT NULL,
	`mat_khau`			varchar(250) NOT NULL,  
	PRIMARY KEY (`admin_id`)
);

DROP TABLE IF EXISTS bai_viet;
CREATE TABLE `bai_viet` (
	`baiviet_id`		int NOT NULL AUTO_INCREMENT,
    `ten_tacgia` 		varchar(50) NOT NULL,
    `email_tacgia` 		varchar(50) NOT NULL,
    `thoigian_dang`		DATETIME NOT NULL,
    `khu_vuc` 			varchar(50) NOT NULL,
    `tieu_de`			text,
    `mo_ta`				text,
    `hinh_anh`			LONGBLOB NOT NULL,
    `van_ban`			text,
    `luot_xem`			int,
    `id_ad`				int,
    `thoi_gian_duyet`	DATETIME NOT NULL,
    PRIMARY KEY (`baiviet_id`)
);






