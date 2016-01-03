#!/bin/bash

cat <<EOF | sqlite3 sample-db.timeorg-backup
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE times (id INTEGER PRIMARY KEY AUTOINCREMENT, LoginTime DATETIME, LogoutTime DATETIME);
INSERT INTO "times" VALUES(1,'2016-01-01 08:16:00','2012-01-01 12:16:00');
INSERT INTO "times" VALUES(2,'2016-01-01 13:20:00','2012-01-01 17:20:00');
INSERT INTO "times" VALUES(3,'2016-01-02 08:10:00','2012-01-02 12:05:00');
INSERT INTO "times" VALUES(4,'2016-01-02 13:00:00','2012-01-02 17:05:00');
CREATE TABLE times_statistic (date DATE PRIMARY KEY, work INTEGER, pause INTEGER);
INSERT INTO "times_statistic" VALUES('2016-01-01 00:00:00',28800,3600);
INSERT INTO "times_statistic" VALUES('2016-01-02 00:00:00',28800,3600);
CREATE TABLE daily_tags (date DATE PRIMARY KEY, note TEXT, flags INTEGER, halfDay boolean);
INSERT INTO "daily_tags" VALUES('2016-01-01 00:00:00','First day of the year',0,0);
DELETE FROM sqlite_sequence;
INSERT INTO "sqlite_sequence" VALUES('times',5);
CREATE INDEX LoginTimeIdx ON times (LoginTime ASC);
COMMIT;
EOF
