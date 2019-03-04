/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50720
Source Host           : localhost:3306
Source Database       : movie

Target Server Type    : MYSQL
Target Server Version : 50720
File Encoding         : 65001

Date: 2018-09-30 19:28:30
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `is_super` smallint(6) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `role_id` (`role_id`),
  KEY `ix_admin_add_time` (`add_time`),
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES ('2', 'chen', 'pbkdf2:sha256:50000$kDlmzQfe$14607416c55327099d6926c4628296f58578700550a9060c696893b903ec9309', '0', '4', '2018-09-26 16:19:12');
INSERT INTO `admin` VALUES ('3', '小刘', 'pbkdf2:sha256:50000$bsAOuO6m$8b5209b55550c95fbe5db328428717f739ead60f562c639b581985eb0c5401d7', null, '4', '2018-09-27 20:31:56');

-- ----------------------------
-- Table structure for admin_log
-- ----------------------------
DROP TABLE IF EXISTS `admin_log`;
CREATE TABLE `admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_admin_log_add_time` (`add_time`),
  CONSTRAINT `admin_log_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of admin_log
-- ----------------------------
INSERT INTO `admin_log` VALUES ('1', '2', '127.0.0.1', '2018-09-27 18:39:00');
INSERT INTO `admin_log` VALUES ('2', '2', '127.0.0.1', '2018-09-27 18:39:09');
INSERT INTO `admin_log` VALUES ('3', '2', '127.0.0.1', '2018-09-29 16:38:14');
INSERT INTO `admin_log` VALUES ('4', '2', '127.0.0.1', '2018-09-29 17:51:55');

-- ----------------------------
-- Table structure for auth
-- ----------------------------
DROP TABLE IF EXISTS `auth`;
CREATE TABLE `auth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `url` (`url`),
  KEY `ix_auth_add_time` (`add_time`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth
-- ----------------------------
INSERT INTO `auth` VALUES ('1', '添加标签', '/admin/tag/add', '2018-09-27 19:02:14');
INSERT INTO `auth` VALUES ('2', '删除标签', '/admin/tag/del/<int:id>', '2018-09-27 19:07:00');

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text,
  `movie_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_comment_add_time` (`add_time`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of comment
-- ----------------------------
INSERT INTO `comment` VALUES ('1', '好看', '1', '3', '2018-09-27 16:25:43');
INSERT INTO `comment` VALUES ('3', '<p><img src=\"http://img.baidu.com/hi/bobo/B_0005.gif\"/>真好看哦</p>', '5', '4', '2018-09-29 20:18:29');
INSERT INTO `comment` VALUES ('4', '<p><img src=\"http://img.baidu.com/hi/jx2/j_0002.gif\"/></p>', '5', '4', '2018-09-29 20:18:42');

-- ----------------------------
-- Table structure for movie
-- ----------------------------
DROP TABLE IF EXISTS `movie`;
CREATE TABLE `movie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `info` text,
  `logo` varchar(255) DEFAULT NULL,
  `star` smallint(6) DEFAULT NULL,
  `play_num` bigint(20) DEFAULT NULL,
  `comment_num` bigint(20) DEFAULT NULL,
  `tag_id` int(11) DEFAULT NULL,
  `area` varchar(255) DEFAULT NULL,
  `release_time` date DEFAULT NULL,
  `length` varchar(100) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `url` (`url`),
  UNIQUE KEY `logo` (`logo`),
  KEY `tag_id` (`tag_id`),
  KEY `ix_movie_add_time` (`add_time`),
  CONSTRAINT `movie_ibfk_1` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of movie
-- ----------------------------
INSERT INTO `movie` VALUES ('1', '真厉害啊', '2018092916392675e68bee9f76441a9d688e1b417398fe.jpg', '666666666666666', '20180929163926b620d52d700244919f871b9c48f84ef4.jpg', '4', '9', '0', '8', '中国', '2018-09-06', '10', '2018-09-26 19:45:39');
INSERT INTO `movie` VALUES ('3', '5555555555', '20180927134346478f5d573edf4c4b9d784b37c8c82276.jpg', '555555555', '201809271343464c02c214c59a4be4b27838a01892640f.jpg', '2', '47', '0', '10', '中国', '2018-09-13', '10', '2018-09-27 13:43:46');
INSERT INTO `movie` VALUES ('5', '4444444', '20180927143007ab312ce7304f4bec893713274734abe4.jpg', '345677', '201809271430076c5c1790cf3948e0ba4be5819850345b.jpg', '5', '29', '2', '1', '中国', '2018-09-13', '10', '2018-09-27 14:12:30');
INSERT INTO `movie` VALUES ('6', '星球大战', '20180929194634ea93e9fd4977490ea36afa5fbaf1cf31.ogg', '星球大战', '201809291946346982a84ae64046888079306fce22c895.jpg', '3', '11', '0', '11', '美国', '2018-09-21', '15', '2018-09-29 19:46:35');

-- ----------------------------
-- Table structure for movie_col
-- ----------------------------
DROP TABLE IF EXISTS `movie_col`;
CREATE TABLE `movie_col` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_movie_col_add_time` (`add_time`),
  CONSTRAINT `movie_col_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`),
  CONSTRAINT `movie_col_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of movie_col
-- ----------------------------
INSERT INTO `movie_col` VALUES ('1', '3', '4', '2018-09-30 15:37:07');
INSERT INTO `movie_col` VALUES ('2', '1', '4', '2018-09-30 15:48:21');
INSERT INTO `movie_col` VALUES ('3', '6', '4', '2018-09-30 15:59:53');

-- ----------------------------
-- Table structure for op_log
-- ----------------------------
DROP TABLE IF EXISTS `op_log`;
CREATE TABLE `op_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `reason` varchar(600) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_op_log_add_time` (`add_time`),
  CONSTRAINT `op_log_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of op_log
-- ----------------------------
INSERT INTO `op_log` VALUES ('1', '2', '127.0.0.1', '添加标签haha成功', '2018-09-27 18:31:23');

-- ----------------------------
-- Table structure for preview
-- ----------------------------
DROP TABLE IF EXISTS `preview`;
CREATE TABLE `preview` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `logo` (`logo`),
  KEY `ix_preview_add_time` (`add_time`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of preview
-- ----------------------------
INSERT INTO `preview` VALUES ('1', '变形金刚', '201809271514048355520be3e9441fb4c44a47e5b725b0.jpg', '2018-09-27 15:14:04');
INSERT INTO `preview` VALUES ('2', '变形1', '201809271541208ec3ea7353e547a98dbc1bc25982e3a8.jpg', '2018-09-27 15:38:18');
INSERT INTO `preview` VALUES ('3', '变形2', '201809291752150f97b6ec8165437890c2c29aa9ab9fc6.jpg', '2018-09-29 17:52:16');
INSERT INTO `preview` VALUES ('4', '变形3', '20180929175230199c76b346ac4f59bbad98451a5fb566.jpg', '2018-09-29 17:52:30');
INSERT INTO `preview` VALUES ('5', '变形5', '20180929175239b8576621ff144a268294cf323231b0c1.jpg', '2018-09-29 17:52:40');

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `auths` varchar(600) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_role_add_time` (`add_time`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES ('2', '标签管理员', '1,2', '2018-09-27 19:39:35');
INSERT INTO `role` VALUES ('4', '标签管理员1', '1', '2018-09-27 20:21:25');

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_tag_add_time` (`add_time`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of tag
-- ----------------------------
INSERT INTO `tag` VALUES ('1', '动作', '2018-09-26 17:05:45');
INSERT INTO `tag` VALUES ('2', '爱情', '2018-09-26 17:07:18');
INSERT INTO `tag` VALUES ('3', '悬疑', '2018-09-26 17:08:35');
INSERT INTO `tag` VALUES ('4', '动画', '2018-09-26 17:36:37');
INSERT INTO `tag` VALUES ('5', '冒险', '2018-09-26 17:36:43');
INSERT INTO `tag` VALUES ('6', '灾难', '2018-09-26 17:37:06');
INSERT INTO `tag` VALUES ('7', '武侠', '2018-09-26 17:37:10');
INSERT INTO `tag` VALUES ('8', '犯罪', '2018-09-26 17:49:44');
INSERT INTO `tag` VALUES ('9', '音乐', '2018-09-26 17:49:49');
INSERT INTO `tag` VALUES ('10', '惊悚', '2018-09-26 17:49:55');
INSERT INTO `tag` VALUES ('11', '战争', '2018-09-26 17:50:14');
INSERT INTO `tag` VALUES ('12', '历史', '2018-09-26 17:50:19');
INSERT INTO `tag` VALUES ('17', '游戏', '2018-09-26 18:24:40');
INSERT INTO `tag` VALUES ('18', 'hha', '2018-09-27 18:30:46');
INSERT INTO `tag` VALUES ('19', 'haha', '2018-09-27 18:31:23');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `info` text,
  `face` varchar(255) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  `uuid` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `face` (`face`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_user_add_time` (`add_time`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('3', '大陈', '1234567', '1234567@qq.com', '12345678902', '6666', '20180927134407c22d179ccada4ad7a332fa6d3a2b0063.jpg', '2018-09-27 16:16:16', null);
INSERT INTO `user` VALUES ('4', '小李子', 'pbkdf2:sha256:50000$GBrjHOIz$a6dab930e49d07b8d830dcda656cad5f6dfaa9d8fc7d099fcebb1f5556ebfce6', '123@qq.com', '13345678970', '真帅啊', '201809291710215bdbc16ea2e74c319aedea3ba596c292.jpg', '2018-09-29 14:54:12', '2306c37c790e4a8e95ef1bd6c3523663');

-- ----------------------------
-- Table structure for user_log
-- ----------------------------
DROP TABLE IF EXISTS `user_log`;
CREATE TABLE `user_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_user_log_add_time` (`add_time`),
  CONSTRAINT `user_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user_log
-- ----------------------------
INSERT INTO `user_log` VALUES ('1', '3', '192.168.0.1', '2018-09-27 18:47:41');
INSERT INTO `user_log` VALUES ('2', '3', '192.168.0.2', '2018-09-27 18:47:59');
INSERT INTO `user_log` VALUES ('3', '4', '127.0.0.1', '2018-09-29 15:05:10');
INSERT INTO `user_log` VALUES ('4', '4', '127.0.0.1', '2018-09-29 15:08:39');
INSERT INTO `user_log` VALUES ('5', '4', '127.0.0.1', '2018-09-29 15:12:27');
INSERT INTO `user_log` VALUES ('6', '4', '127.0.0.1', '2018-09-29 15:14:13');
INSERT INTO `user_log` VALUES ('7', '4', '127.0.0.1', '2018-09-29 15:15:51');
INSERT INTO `user_log` VALUES ('8', '4', '127.0.0.1', '2018-09-29 15:35:06');
INSERT INTO `user_log` VALUES ('9', '4', '127.0.0.1', '2018-09-29 15:35:37');
INSERT INTO `user_log` VALUES ('10', '4', '127.0.0.1', '2018-09-29 15:36:11');
INSERT INTO `user_log` VALUES ('11', '4', '127.0.0.1', '2018-09-29 15:41:22');
INSERT INTO `user_log` VALUES ('12', '4', '127.0.0.1', '2018-09-29 17:00:50');
INSERT INTO `user_log` VALUES ('13', '4', '127.0.0.1', '2018-09-29 17:23:17');
INSERT INTO `user_log` VALUES ('14', '4', '127.0.0.1', '2018-09-29 17:25:00');
INSERT INTO `user_log` VALUES ('15', '4', '127.0.0.1', '2018-09-29 19:51:49');
INSERT INTO `user_log` VALUES ('16', '4', '127.0.0.1', '2018-09-29 19:55:59');
INSERT INTO `user_log` VALUES ('17', '4', '127.0.0.1', '2018-09-30 13:30:02');
INSERT INTO `user_log` VALUES ('18', '4', '127.0.0.1', '2018-09-30 13:42:10');
