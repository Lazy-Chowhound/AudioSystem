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

