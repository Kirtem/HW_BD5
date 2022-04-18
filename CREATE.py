CREATE TABLE IF NOT EXISTS Singers (
	id serial primary key,
	singer_nickname varchar(100) not null
);

CREATE TABLE IF NOT EXISTS AlbumSing (
	id serial primary key,
	id_singer integer references singers(id),
	id_albums integer references albums(id)
);

CREATE TABLE IF NOT EXISTS Albums (
	id serial primary key,
	album_name varchar(50) not null,
	album_year integer not null
);

CREATE TABLE IF NOT EXISTS Songs (
	id serial primary key,
	song_name varchar(50) not null,
	song_time numeric not null,
	album_id integer references albums(id)
);

CREATE TABLE IF NOT EXISTS CollectionSongs (
	id serial primary key,
	id_song integer references songs(id),
	id_collection integer references collection(id)
);

CREATE TABLE IF NOT EXISTS Collection (
	id serial primary key,
	collection_name varchar(50) not null,
	collectin_year integer not null
);z

CREATE TABLE IF NOT EXISTS Genres (
	id serial primary key,
	genres_name varchar(50) not null
);


CREATE TABLE IF NOT EXISTS GenresSing (
	id serial primary key,
	id_singer integer references singers(id),
	id_genres integer references genres(id)
);
