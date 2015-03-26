drop table if exists users;
create table users (
  username string(128) not null primary key,
  password string(128) not null,
  email string(128) not null
);

drop table if exists symptoms;
create table symptoms (
  username string(128) not null,
  primary_symptom text not null,
  secondary_symptom text not null,
  created datetime not null,
  FOREIGN KEY(username) REFERENCES users(username)
);

drop table if exists addresses;
create table addresses (
  username string(128) not null,
  addr_one text not null,
  addr_two text not null,
  city string(128) not null,
  state string(128) not null,
  zip string(128) not null,
  phone datetime not null,
  FOREIGN KEY(username) REFERENCES users(username)
);
