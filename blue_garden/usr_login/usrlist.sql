drop table if exists usrlist;
create table usrlist (
  usrname text primary key,
  usrpass text not null,
  usrtype text not null
);
