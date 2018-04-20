drop table if exists checked_on;
drop table if exists game_versions;
drop table if exists launcher_versions;

drop index if exists game_date;
drop index if exists launcher_date;

create table game_versions (
  hash varchar(32) primary key,
  version varchar(64) not null unique,
  url text not null,
  entered_on timestamp not null
);
create index game_date on game_versions (entered_on);

create table launcher_versions (
  hash varchar(32) primary key,
  version varchar(64) not null unique,
  url text not null,
  entered_on timestamp not null
);
create index launcher_date on launcher_versions (entered_on);

create table checked_on (
  id integer primary key,
  checked_on timestamp not null
);
