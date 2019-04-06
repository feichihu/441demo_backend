CREATE TABLE Users (
    u_id NUMBER,
    username VARCHAR(100), 
    token INTEGER,
    img_id INTEGER,
    level INTEGER,
    PRIMARY KEY (u_id));

CREATE TABLE Friends (
    u1_id NUMBER,
    u2_id NUMBER,
    PRIMARY KEY (u1_id, u2_id),
    FOREIGN KEY (u1_id) REFERENCES users(u_id),
    FOREIGN KEY (u2_id) REFERENCES users(u_id));

CREATE TABLE Songs (
    s_id NUMBER,
    u_id NUMBER,
    sing_time TIMESTAMP,
    duration VARCHAR(100),
    score INTEGER,
    album_name VARCHAR(100), 
    PRIMARY KEY (u_id));

CREATE TRIGGER order_friends_pairs
BEFORE INSERT ON FRIENDS
FOR EACH ROW
DECLARE temp NUMBER;
BEGIN
IF :NEW.USER1_ID > :NEW.USER2_ID THEN
temp := :NEW.USER2_ID;
:NEW.USER2_ID := :NEW.USER1_ID;
:NEW.USER1_ID := temp;
END IF;
END;
/


