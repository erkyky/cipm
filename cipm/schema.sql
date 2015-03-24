drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text not null,
  password text not null
);

drop table if exists symptoms;
create table symptoms (
  id integer primary key autoincrement,
  userid integer not null,
  primary_symptom text not null,
  secondary_symptom text not null,
  created datetime not null,
  FOREIGN KEY(userid) REFERENCES users(id)
);

drop table if exists addresses;
create table addresses (
  id integer primary key autoincrement,
  userid integer not null,
  addr_one text not null,
  addr_two text not null,
  city text not null,
  state text not null,
  zip text not null,
  phone datetime not null,
  FOREIGN KEY(userid) REFERENCES users(id)
);
