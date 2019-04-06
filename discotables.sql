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
    PRIMARY KEY (u_id));



