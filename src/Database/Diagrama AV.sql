CREATE TABLE "Drivers" (
  "driver_id" UUID PRIMARY KEY,
  "first_name" varchar,
  "middle_name" varchar,
  "last_name_1" varchar,
  "last_name_2" varchar,
  "rfc" varchar,
  "phone" varchar,
  "birthday" date,
  "is_current" boolean,
  "score" numeric,
  "blood_type" varchar,
  "emergency_contact" UUID,
  "photo" bytea,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "EmergencyContacts" (
  "emergency_contact_id" UUID PRIMARY KEY,
  "first_name" varchar,
  "last_name" varchar,
  "middle_name" varchar,
  "phone" varchar
);

CREATE TABLE "Fleet" (
  "fleet_id" UUID PRIMARY KEY,
  "fleet_name" varchar,
  "created_at" timestamp
);

CREATE TABLE "MotorStatuses" (
  "motor_status_id" UUID PRIMARY KEY,
  "motor_status_value" varchar,
  "motor_status_description" varchar
);

CREATE TABLE "Models" (
  "model_id" UUID PRIMARY KEY,
  "model_name" varchar,
  "created_at" timestamp
);

CREATE TABLE "Units" (
  "unit_id" UUID PRIMARY KEY,
  "driver" UUID,
  "fleet" UUID,
  "model" UUID,
  "motor_status" UUID,
  "fuel_level" numeric,
  "current_speed" numeric,
  "is_online" boolean,
  "panic_button_active" boolean,
  "created_at" timestamp,
  "updated_at" timestamp,
  "rpm" int,
  "temperature" int,
  "check_engine" boolean
);

CREATE TABLE "SpeedHistory" (
  "speed_id" UUID PRIMARY KEY,
  "unit_id" UUID,
  "driver_id" UUID,
  "speed" numeric,
  "recorded_at" timestamp
);

CREATE TABLE "LocationHistory" (
  "location_id" UUID PRIMARY KEY,
  "unit_id" UUID,
  "driver_id" UUID,
  "latitude" numeric,
  "longitude" numeric,
  "recorded_at" timestamp
);

CREATE TABLE "DailyReport" (
  "daily_report_id" UUID PRIMARY KEY,
  "unit" UUID,
  "max_speed" UUID,
  "driver" UUID,
  "speed_limit_reached" int,
  "conduction_time" numeric,
  "sudden_accelerations" int,
  "sudden_brakes" int,
  "sudden_turns" int,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "Notifications" (
  "notification_id" UUID PRIMARY KEY,
  "notification_type" UUID,
  "unit" UUID,
  "detail" varchar,
  "created_at" timestamp
);

CREATE TABLE "NotificationTypes" (
  "notification_type_id" UUID PRIMARY KEY,
  "notification_value" varchar,
  "created_at" timestamp
);

ALTER TABLE "Drivers" ADD FOREIGN KEY ("emergency_contact") REFERENCES "EmergencyContacts" ("emergency_contact_id");

ALTER TABLE "Units" ADD FOREIGN KEY ("driver") REFERENCES "Drivers" ("driver_id");

ALTER TABLE "Units" ADD FOREIGN KEY ("fleet") REFERENCES "Fleet" ("fleet_id");

ALTER TABLE "Units" ADD FOREIGN KEY ("model") REFERENCES "Models" ("model_id");

ALTER TABLE "Units" ADD FOREIGN KEY ("motor_status") REFERENCES "MotorStatuses" ("motor_status_id");

ALTER TABLE "SpeedHistory" ADD FOREIGN KEY ("unit_id") REFERENCES "Units" ("unit_id");

ALTER TABLE "SpeedHistory" ADD FOREIGN KEY ("driver_id") REFERENCES "Drivers" ("driver_id");

ALTER TABLE "LocationHistory" ADD FOREIGN KEY ("unit_id") REFERENCES "Units" ("unit_id");

ALTER TABLE "LocationHistory" ADD FOREIGN KEY ("driver_id") REFERENCES "Drivers" ("driver_id");

ALTER TABLE "DailyReport" ADD FOREIGN KEY ("unit") REFERENCES "Units" ("unit_id");

ALTER TABLE "DailyReport" ADD FOREIGN KEY ("driver") REFERENCES "Drivers" ("driver_id");

ALTER TABLE "Notifications" ADD FOREIGN KEY ("unit") REFERENCES "Units" ("unit_id");

ALTER TABLE "Notifications" ADD FOREIGN KEY ("notification_type") REFERENCES "NotificationTypes" ("notification_type_id");
