begin;

create table survey (
    id bigserial not null,
        primary key (id),
    surveyid text not null,
        unique (surveyid),
    tracked boolean not null,
    last_responseid text
);

create table follow_up (
    id bigserial not null,
        primary key (id),
    baseline_id bigint not null,
        foreign key (baseline_id) references survey (id),
    followupid text not null,
        unique (followupid),
    rank bigint not null,
        unique (baseline_id, rank),
    messageid text not null,
        check (messageid <> '')
    time_interval text not null,
        check (time_interval <> '')
);

create table response (
    id bigserial not null,
        primary key (id),
    responseid text not null,
        unique (responseid)
);

create table panel (
    id bigserial not null,
        primary key (id),
    panelid text not null,
        unique (panelid),
    surveyid text not null,
    invited boolean not null
);

create index panel_invited on panel (invited);

commit;

