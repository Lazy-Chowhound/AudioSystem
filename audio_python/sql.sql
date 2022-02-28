create table audiosetproperty
(
    id           int auto_increment
        primary key,
    name         varchar(50)   not null,
    language     varchar(20)   not null,
    size         varchar(10)   not null,
    hour         int           not null,
    people       int           not null,
    form         varchar(10)   not null,
    distribution varchar(1000) not null
);

create table ModelUploadHistory
(
    id   int auto_increment,
    name varchar(100) not null,
    time datetime     not null,
    constraint ModelUploadHistory_pk
        primary key (id)
);

