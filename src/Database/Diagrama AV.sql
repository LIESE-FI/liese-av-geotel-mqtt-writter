CREATE TABLE "sites" (
  "id" int PRIMARY KEY,
  "name" text UNIQUE
);

CREATE TABLE "companies" (
  "id" int PRIMARY KEY,
  "name" text UNIQUE
);

CREATE TABLE "controllers" (
  "id" int PRIMARY KEY,
  "name" text UNIQUE
);

CREATE TABLE "devices" (
  "id" int PRIMARY KEY,
  "device_id" text UNIQUE,
  "site_id" int,
  "company_id" int,
  "controller_id" int
);

CREATE TABLE "measurements" (
  "id" bigint PRIMARY KEY,
  "device_id" int,
  "timestamp" timestamp,
  "modbus_address" int
);

CREATE TABLE "measurement_values" (
  "id" bigint PRIMARY KEY,
  "measurement_id" bigint,
  "name" text,
  "address" int,
  "value" double,
  "type" text,
  "status" text
);

CREATE TABLE "binary_states" (
  "id" bigint PRIMARY KEY,
  "measurement_id" bigint,
  "gcb_feedback" boolean,
  "mcb_feedback" boolean,
  "ready_to_load" boolean,
  "generator_healthy" boolean,
  "mains_healthy" boolean,
  "warning_alarm" boolean,
  "shutdown_alarm" boolean,
  "status" text
);

CREATE TABLE "setpoints" (
  "id" bigint PRIMARY KEY,
  "measurement_id" bigint,
  "name" text,
  "address" int,
  "value" double,
  "status" text
);

CREATE TABLE "alarms" (
  "id" bigint PRIMARY KEY,
  "measurement_id" bigint,
  "alarm_index" int,
  "address" int,
  "text" text,
  "status" text
);

ALTER TABLE "devices" ADD FOREIGN KEY ("site_id") REFERENCES "sites" ("id");

ALTER TABLE "devices" ADD FOREIGN KEY ("company_id") REFERENCES "companies" ("id");

ALTER TABLE "devices" ADD FOREIGN KEY ("controller_id") REFERENCES "controllers" ("id");

ALTER TABLE "measurements" ADD FOREIGN KEY ("device_id") REFERENCES "devices" ("id");

ALTER TABLE "measurement_values" ADD FOREIGN KEY ("measurement_id") REFERENCES "measurements" ("id");

ALTER TABLE "binary_states" ADD FOREIGN KEY ("measurement_id") REFERENCES "measurements" ("id");

ALTER TABLE "setpoints" ADD FOREIGN KEY ("measurement_id") REFERENCES "measurements" ("id");

ALTER TABLE "alarms" ADD FOREIGN KEY ("measurement_id") REFERENCES "measurements" ("id");
