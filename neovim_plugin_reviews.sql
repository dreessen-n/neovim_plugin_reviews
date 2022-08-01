-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema neovim_plugin_reviews
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `neovim_plugin_reviews` ;

-- -----------------------------------------------------
-- Schema neovim_plugin_reviews
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `neovim_plugin_reviews` DEFAULT CHARACTER SET utf8 ;
USE `neovim_plugin_reviews` ;

-- -----------------------------------------------------
-- Table `neovim_plugin_reviews`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `neovim_plugin_reviews`.`users` ;

CREATE TABLE IF NOT EXISTS `neovim_plugin_reviews`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(50) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `neovim_plugin_reviews`.`reviews`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `neovim_plugin_reviews`.`reviews` ;

CREATE TABLE IF NOT EXISTS `neovim_plugin_reviews`.`reviews` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `category` VARCHAR(255) NULL,
  `content` TEXT(900) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW() ON UPDATE NOW(),
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_recipes_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_recipes_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `neovim_plugin_reviews`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `neovim_plugin_reviews`.`likes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `neovim_plugin_reviews`.`likes` ;

CREATE TABLE IF NOT EXISTS `neovim_plugin_reviews`.`likes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `review_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_favorited_reviews_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_favorited_reviews_reviews1_idx` (`review_id` ASC) VISIBLE,
  CONSTRAINT `fk_favorited_reviews_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `neovim_plugin_reviews`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_favorited_reviews_reviews1`
    FOREIGN KEY (`review_id`)
    REFERENCES `neovim_plugin_reviews`.`reviews` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `neovim_plugin_reviews`.`comments`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `neovim_plugin_reviews`.`comments` ;

CREATE TABLE IF NOT EXISTS `neovim_plugin_reviews`.`comments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `comment` TEXT(600) NULL,
  `user_id` INT NOT NULL,
  `review_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_comments_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_comments_reviews1_idx` (`review_id` ASC) VISIBLE,
  CONSTRAINT `fk_comments_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `neovim_plugin_reviews`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_comments_reviews1`
    FOREIGN KEY (`review_id`)
    REFERENCES `neovim_plugin_reviews`.`reviews` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
