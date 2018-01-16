--- List of known agents
create table agents(
    agent_id int not null primary key auto_increment,
    agent_ip int not null,
    agent_port int not null default 36788,
    agent_version float not null,
    is_online tinyint default 0,
    agent_uuid binary(16)
);
