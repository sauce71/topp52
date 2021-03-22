-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS tours;
DROP TABLE IF EXISTS users;

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;


CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(50) NOT NULL,
  admin BOOLEAN NOT NULL DEFAULT 0,
  visible BOOLEAN NOT NULL DEFAULT 1,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  initial_tours INTEGER NOT NULL DEFAULT 0
);


CREATE TABLE tours (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    tour_date DATE NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
    ON DELETE CASCADE
);




CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

 
