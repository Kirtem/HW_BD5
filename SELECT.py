import sqlalchemy
import psycopg2
engine = sqlalchemy.create_engine('postgresql://postgres:admin@localhost:5432/py48')

connection = engine.connect()

# количество исполнителей в каждом жанре;
print(connection.execute("""SELECT g.genres_name, COUNT(gs.id_singer) FROM GenresSing GS
LEFT JOIN Genres G ON gs.id_genres = g.id
GROUP BY genres_name;
""").fetchall())

# количество треков, вошедших в альбомы 2019-2020 годов;
print(connection.execute("""SELECT a.album_name, COUNT(s.id) FROM Songs S
LEFT JOIN Albums a ON s.album_id = a.id
WHERE album_year BETWEEN 2019 AND 2020
GROUP BY album_name;
""").fetchall())

# средняя продолжительность треков по каждому альбому;
print(connection.execute("""SELECT a.album_name, AVG(s.song_time) FROM Songs S
LEFT JOIN Albums a ON s.album_id = a.id
GROUP BY album_name;
""").fetchall())

# все исполнители, которые не выпустили альбомы в 2020 году;
print(connection.execute("""SELECT s.singer_nickname FROM Singers S
JOIN Albumsing als ON s.id = als.id_singer
JOIN Albums a ON als.id_albums = a.id
WHERE a.album_year != 2020;
""").fetchall())

# названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
print(connection.execute("""SELECT c.collection_name FROM Collection c
LEFT JOIN Collectionsongs cs ON c.id = cs.id_collection
LEFT JOIN Songs sn ON sn.id = cs.id_song
LEFT JOIN Albums a ON a.id = sn.album_id
LEFT JOIN Albumsing als ON als.id_albums = a.id
LEFT JOIN Singers s ON s.id = als.id_singer
WHERE s.singer_nickname = 'Aria';
""").fetchall())

# название альбомов, в которых присутствуют исполнители более 1 жанра;
print(connection.execute("""SELECT a.album_name FROM Albums a
LEFT JOIN Albumsing als ON als.id_albums = a.id
LEFT JOIN Singers s ON s.id = als.id_singer
LEFT JOIN Genressing gs ON gs.id_singer = s.id
GROUP BY a.album_name
HAVING COUNT(gs.id_genres) > 1;
""").fetchall())

# наименование треков, которые не входят в сборники;
print(connection.execute("""SELECT s.song_name FROM Songs s
LEFT JOIN Collectionsongs cs ON cs.id_song = s.id
GROUP BY s.song_name
HAVING COUNT(cs.id_song) = 0;
""").fetchall())

# исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);
print(connection.execute("""SELECT s.song_time, s.song_name, singer_nickname FROM Singers sn
LEFT JOIN Albumsing als ON als.id_singer = sn.id
LEFT JOIN Albums a ON a.id = als.id_albums
LEFT JOIN Songs s ON s.album_id = a.id
WHERE s.song_time = (SELECT MIN(song_time) FROM Songs)
GROUP BY s.song_name, s.song_time, sn.singer_nickname;
""").fetchall())

# название альбомов, содержащих наименьшее количество треков.
print(connection.execute("""SELECT a.album_name FROM Albums a
LEFT JOIN Songs s ON s.album_id = a.id
WHERE s.album_id in (
     SELECT album_id from Songs
     GROUP BY album_id
     HAVING COUNT(album_id) = 1);
""").fetchall())
