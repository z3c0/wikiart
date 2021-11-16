--Create dimension tables
DROP TABLE IF EXISTS dim_work;
CREATE TABLE dim_work (
  work_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  work_title TEXT NOT NULL,
  work_url TEXT NOT NULL
);
DROP TABLE IF EXISTS dim_artist;
CREATE TABLE dim_artist (
  artist_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  artist_name VARCHAR(250) NOT NULL,
  artist_url TEXT NOT NULL,
  genre TEXT NULL,
  century TEXT NULL,
  institution TEXT NULL,
  field TEXT NULL,
  nationality TEXT NULL
);
-- Create fact tables
DROP TABLE IF EXISTS fact_artist_works;
CREATE TABLE fact_artist_works (
  artist_id INT UNSIGNED NOT NULL,
  work_id INT UNSIGNED NOT NULL
);