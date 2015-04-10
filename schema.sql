drop table if exists users;
create table users (
  username string(128) not null primary key,
  password string(128) not null,
  email string(128) not null
);

drop table if exists symptoms;
create table symptoms (
  username string(128) not null,
  symptom text not null,
  details text not null,
  extra text not null,
  reported datetime not null,
  FOREIGN KEY(username) REFERENCES users(username)
);

drop table if exists addresses;

drop table if exists passport;
create table passport (
  username string(128) not null,
  firstname string(128) not null,
  --middlename string(128) not null,
  surname string(128) not null,
  --addr_one text not null,
  --addr_two text not null,
  city string(128) not null,
  state string(128) not null,
  --zip string(128) not null,
  phone text not null,
  FOREIGN KEY(username) REFERENCES users(username)
);
