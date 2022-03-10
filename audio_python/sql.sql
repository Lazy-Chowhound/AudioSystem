create table audiosetproperty
(
    id           int auto_increment
        primary key,
    name         varchar(50)   not null,
    language     varchar(20)   not null,
    size         varchar(10)   not null,
    hour         float         not null,
    people       int           not null,
    form         varchar(10)   not null,
    distribution varchar(1000) not null
);

create table modelHistory
(
    id   int auto_increment,
    name varchar(100) not null,
    time datetime     not null,
    constraint ModelUploadHistory_pk
        primary key (id)
);

create table datasetHistory
(
    id   int auto_increment,
    name varchar(50) not null,
    time datetime    not null,
    user varchar(100) not null;
    constraint datasetHistory_pk
        primary key (id)
);

create table operationhistory
(
    id         int auto_increment
        primary key,
    dataset    varchar(50)  not null,
    audioName  varchar(100) not null,
    time       datetime     not null,
    formerType varchar(100) not null,
    latterType varchar(100) not null
);

create table action
(
    id          int auto_increment
        primary key,
    action_code varchar(100) null,
    action_name varchar(100) not null
);

create table module
(
    id          int auto_increment
        primary key,
    module_code varchar(100) not null,
    module_name varchar(100) not null
);

create table permission
(
    id              int auto_increment
        primary key,
    permission_name varchar(100) not null,
    module_id       int          not null,
    action_id       int          not null
);

create table role
(
    id          int auto_increment,
    role_name   varchar(100) null,
    permissions json         not null,
    constraint role_pk
        primary key (id)
);

create table user
(
    id       int auto_increment
        primary key,
    name     varchar(255) not null,
    password varchar(255) not null,
    role     json         not null
);



