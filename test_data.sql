pragma foreign_keys=OFF;
begin transaction;

insert into contest values (1, "deutsch");
insert into contest values (2, "english");

insert into descriptors values (1, "loyal", 1);
insert into descriptors values (2, "diplomatisch", 1);
insert into descriptors values (3, "unterstützend", 1);
insert into descriptors values (4, "sozial", 1);
insert into descriptors values (5, "idealistisch", 1);
insert into descriptors values (6, "innovativ", 1);
insert into descriptors values (7, "pfiffig", 1);
insert into descriptors values (8, "unabhängig", 1);
insert into descriptors values (9, "analytisch", 1);
insert into descriptors values (10, "selbstlos", 1);
insert into descriptors values (11, "mutig", 1);
insert into descriptors values (12, "unkonventionell", 1);
insert into descriptors values (13, "vertrauenswürdig", 1);
insert into descriptors values (14, "spielerisch", 1);
insert into descriptors values (15, "aufrichtig", 1);
insert into descriptors values (16, "cool", 1);
insert into descriptors values (17, "fortschrittlich", 1);
insert into descriptors values (18, "kritisch", 1);
insert into descriptors values (19, "rational", 1);
insert into descriptors values (20, "beständig", 1);

insert into descriptors values (21, "innovative", 2);
insert into descriptors values (22, "idealistic", 2);
insert into descriptors values (23, "smart", 2);
insert into descriptors values (24, "social", 2);
insert into descriptors values (25, "independent", 2);
insert into descriptors values (26, "credible", 2);
insert into descriptors values (27, "analytical", 2);
insert into descriptors values (28, "supportive", 2);
insert into descriptors values (29, "honest", 2);
insert into descriptors values (30, "critical", 2);
insert into descriptors values (31, "rational", 2);
insert into descriptors values (32, "progressive", 2);
insert into descriptors values (33, "unconventional", 2);
insert into descriptors values (34, "courageous", 2);
insert into descriptors values (35, "selfless", 2);
insert into descriptors values (36, "playful", 2);
insert into descriptors values (37, "steady", 2);
insert into descriptors values (38, "charismatic", 2);
insert into descriptors values (39, "wise", 2);
insert into descriptors values (40, "different", 2);

insert into users values (1, "Vera Kreuter");
insert into users values (2, "Martin Häcker");

commit;