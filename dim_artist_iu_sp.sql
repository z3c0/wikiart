DROP PROCEDURE IF EXISTS dim_artist_iu_sp;
CREATE DEFINER = `z3c0` @`192.168.1.%` PROCEDURE `dim_artist_iu_sp`() 
BEGIN

UPDATE
  dim_artist AS da
  INNER JOIN stg_artists AS sa USING(artist_url)
  LEFT JOIN stg_genre_artists AS ga USING(artist_url)
  LEFT JOIN stg_century_artists AS ca USING(artist_url)
  LEFT JOIN stg_school_artists AS sca USING(artist_url)
  LEFT JOIN stg_field_artists AS fa USING(artist_url)
  LEFT JOIN stg_institution_artists AS ia USING(artist_url)
  LEFT JOIN stg_nation_artists AS na USING(artist_url)
  LEFT JOIN stg_genre AS g USING (genre_url)
  LEFT JOIN stg_century AS c USING (century_url)
  LEFT JOIN stg_school AS s USING (school_url)
  LEFT JOIN stg_field AS f USING (field_url)
  LEFT JOIN stg_institution AS i USING (institution_url)
  LEFT JOIN stg_nation AS n USING (nation_url)
SET
  da.genre = g.genre_name,
  da.century = c.century_name,
  da.institution = i.institution_name,
  da.field = f.field_name,
  da.institution = i.institution_name,
  da.nationality = n.nation_name;

INSERT INTO
  dim_artist (artist_name, artist_url)
SELECT
  sa.artist_name,
  sa.artist_url
FROM
  stg_artists AS sa
  LEFT JOIN dim_artist AS da
    ON sa.artist_url = da.artist_url
WHERE
  da.artist_url IS NULL;

END