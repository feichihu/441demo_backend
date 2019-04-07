CREATE TABLE Users (
    u_id INTEGER,
    username VARCHAR(100), 
    token INTEGER,
    img_id INTEGER,
    level INTEGER,
    PRIMARY KEY (u_id));

CREATE TABLE Friends (
    u1_id INTEGER,
    u2_id INTEGER,
    PRIMARY KEY (u1_id, u2_id),
    FOREIGN KEY (u1_id) REFERENCES users(u_id),
    FOREIGN KEY (u2_id) REFERENCES users(u_id));

CREATE TABLE Songs (
    s_id INTEGER,
    u_id INTEGER,
    sing_time TIMESTAMP,
    duration VARCHAR(100),
    score INTEGER,
    album_name VARCHAR(100), 
    PRIMARY KEY (s_id));

INSERT INTO Users (u_id, username, token, img_id, level) VALUES (1, 'llw', 100, 10, 1);
INSERT INTO Users (u_id, username, token, img_id, level) VALUES (2, 'jhe', 200, 5, 1);
INSERT INTO Users (u_id, username, token, img_id, level) VALUES (3, 'cmm', 300, 8, 1);
INSERT INTO Users (u_id, username, token, img_id, level) VALUES (4, 'qyao', 400, 9, 1);
INSERT INTO Users (u_id, username, token, img_id, level) VALUES (5, 'peterz', 500, 15, 1);
INSERT INTO Users (u_id, username, token, img_id, level) VALUES (6, 'fhu', 300, 11, 1);
INSERT INTO Users (u_id, username, token, img_id, level) VALUES (7, 'lurz', 800, 12, 1);

INSERT INTO Friends (u1_id, u2_id) VALUES (1, 2);
INSERT INTO Friends (u1_id, u2_id) VALUES (2, 3);
INSERT INTO Friends (u1_id, u2_id) VALUES (3, 4);
INSERT INTO Friends (u1_id, u2_id) VALUES (5, 6);
INSERT INTO Friends (u1_id, u2_id) VALUES (3, 7);
INSERT INTO Friends (u1_id, u2_id) VALUES (2, 5);

INSERT INTO Songs (s_id, u_id, sing_time, duration, score, album_name) VALUES 
(1, 1, '2019-01-19 20:43:56', '03:04', 2300, 'alphabet');
INSERT INTO Songs (s_id, u_id, sing_time, duration, score, album_name) VALUES 
(2, 1, '2019-02-19 22:33:56', '03:02', 1300, 'alphabet');
INSERT INTO Songs (s_id, u_id, sing_time, duration, score, album_name) VALUES 
(3, 1, '2019-03-19 12:33:56', '03:03', 9300, 'alphabet');
INSERT INTO Songs (s_id, u_id, sing_time, duration, score, album_name) VALUES 
(4, 1, '2019-01-05 13:33:56', '03:10', 4300, 'alphabet');
INSERT INTO Songs (s_id, u_id, sing_time, duration, score, album_name) VALUES 
(5, 1, '2019-01-20 20:33:20', '03:19', 4500, 'alphabet');


