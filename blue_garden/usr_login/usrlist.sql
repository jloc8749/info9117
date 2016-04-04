drop table if exists usrlist;
create table usrlist (
  sessionid integer primary key autoincrement,
  usrname text,--no need to be unique for concurrent logins (is key in dict already)
  usrpass text not null,
  usrtype text not null
);
