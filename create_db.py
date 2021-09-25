from sqlalchemy import create_engine
import datetime

db_url = 'postgresql://gachi_achi:achi_for_gachi@204.2.63.15:10485/achievements'
engine = create_engine(db_url)

engine.execute("""
CREATE TABLE "authentication" (
	"email" varchar(50) NOT NULL,
	"phone" varchar(50) NOT NULL,
	"user_name" varchar(50) NOT NULL,
	"password" varchar(50) NOT NULL,
	"second_anthentication" BOOLEAN NOT NULL,
	CONSTRAINT "authentication_pk" PRIMARY KEY ("email","phone")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "users_main" (
	"user_id" integer NOT NULL,
	"user_name" varchar(50) NOT NULL,
	"email" varchar(50) NOT NULL UNIQUE,
	"phone" varchar(50) NOT NULL UNIQUE,
	CONSTRAINT "users_main_pk" PRIMARY KEY ("user_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "users_information" (
	"user_id" integer NOT NULL,
	"country_id" integer,
	"city_id" integer,
	"sex" varchar,
	"date_born" varchar NOT NULL,
	"age" integer NOT NULL,
	"bio" varchar(50),
	"name" varchar(50) NOT NULL,
	"surname" varchar(50),
	"relation_ship_id" integer[],
	"language_id" integer NOT NULL,
	"wedding" BOOLEAN,
	"communication_conditions" TEXT[],
	"status_work" varchar(50),
	"position" varchar(50),
	"company_id" integer,
	"school_id" integer,
	"bachelor_id" integer,
	"master_id" integer,
	"image_id" integer[],
	CONSTRAINT "users_information_pk" PRIMARY KEY ("user_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "user_statistics" (
	"user_id" integer NOT NULL,
	"friends" integer NOT NULL,
	"likes" integer NOT NULL,
	"comments" integer NOT NULL,
	"reccomendations" integer NOT NULL,
	"achievements" integer NOT NULL,
	"courses" integer NOT NULL,
	CONSTRAINT "user_statistics_pk" PRIMARY KEY ("user_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "user_calendar" (
	"user_id" integer NOT NULL,
	"from_date" timestamp NOT NULL,
	"to_date" timestamp NOT NULL,
	"free" Boolean NOT NULL,
	CONSTRAINT "user_calendar_pk" PRIMARY KEY ("user_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "friends" (
	"relationship_id" integer NOT NULL,
	"user_id" integer NOT NULL UNIQUE,
	"users_id" integer[] NOT NULL,
	"status_id" integer[] NOT NULL,
	"last_update" timestamp NOT NULL,
	CONSTRAINT "friends_pk" PRIMARY KEY ("relationship_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "friend_events" (
	"friend_event_id" integer NOT NULL,
	"relationship_id" integer NOT NULL,
	"user_id_1" integer NOT NULL,
	"user_id_2" integer NOT NULL,
	"update_date" timestamp NOT NULL,
	"status_id" integer NOT NULL,
	CONSTRAINT "friend_events_pk" PRIMARY KEY ("friend_event_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "sessions" (
	"session_id" integer NOT NULL,
	"user_id" integer NOT NULL,
	"from_date" timestamp NOT NULL,
	"to_date" timestamp NOT NULL,
	"duration" integer NOT NULL,
	CONSTRAINT "sessions_pk" PRIMARY KEY ("session_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "images" (
	"image_id" integer NOT NULL,
	"href" TEXT NOT NULL,
	"image_type" varchar(50) NOT NULL,
	CONSTRAINT "images_pk" PRIMARY KEY ("image_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "countries" (
	"country_id" integer NOT NULL,
	"country_name" varchar(50) NOT NULL,
	"country_group" TEXT[] NOT NULL,
	"continent" varchar(50) NOT NULL,
	CONSTRAINT "countries_pk" PRIMARY KEY ("country_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "cities" (
	"city_id" integer NOT NULL,
	"country_id" integer NOT NULL,
	"city_name" varchar(50) NOT NULL,
	"geo" VARCHAR(255) NOT NULL,
	CONSTRAINT "cities_pk" PRIMARY KEY ("city_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "communities" (
	"community_id" integer NOT NULL,
	"wallet_id" integer[],
	"community_type" TEXT NOT NULL,
	"user_id" integer[] NOT NULL,
	"warning_id" integer,
	"accept" BOOLEAN NOT NULL,
	"achievements_get_id" integer[] NOT NULL,
	"achievements_give_id" integer[] NOT NULL,
	"community_name" varchar(50) NOT NULL,
	"country_id" integer NOT NULL,
	"city_id" integer NOT NULL,
	"community_bio" varchar(50),
	"community_conditions" TEXT[] NOT NULL,
	"created_date" timestamp NOT NULL,
	"roles_id" integer[],
	"community_owner_id" integer NOT NULL,
	"image_id" integer NOT NULL,
	CONSTRAINT "communities_pk" PRIMARY KEY ("community_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "community_meetings" (
	"meeting_id" integer NOT NULL,
	"community_id" integer NOT NULL,
	"meeting_type" varchar(50) NOT NULL,
	"meeting_name" varchar(50) NOT NULL,
	"meeting_description" TEXT,
	"conditions_id" integer[],
	"from_date" timestamp NOT NULL,
	"to_date" timestamp NOT NULL,
	"inner" BOOLEAN NOT NULL,
	"online" BOOLEAN NOT NULL,
	"meeting_href" TEXT,
	"meeting_image_id" integer,
	CONSTRAINT "community_meetings_pk" PRIMARY KEY ("meeting_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "community_conditions" (
	"condition_id" integer NOT NULL,
	"community_id" integer NOT NULL,
	"condition_type" TEXT NOT NULL,
	"condition_name" varchar(50) NOT NULL,
	"condition_description" TEXT NOT NULL,
	CONSTRAINT "community_conditions_pk" PRIMARY KEY ("condition_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "community_statistics" (
	"community_id" integer NOT NULL,
	"users" integer NOT NULL,
	"rating" integer NOT NULL,
	"likes" integer NOT NULL,
	"comments" integer NOT NULL,
	"achievements" integer NOT NULL,
	"achievements_give" integer NOT NULL,
	"courses" integer NOT NULL,
	CONSTRAINT "community_statistics_pk" PRIMARY KEY ("community_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "community_roles" (
	"role_id" integer NOT NULL,
	"community_id" integer NOT NULL,
	"role_name" varchar(50) NOT NULL,
	"is_posting" BOOLEAN NOT NULL,
	"is_create_meetings" BOOLEAN,
	"is_accept" BOOLEAN,
	"is_invite" BOOLEAN NOT NULL,
	"is_give_roles" BOOLEAN NOT NULL,
	CONSTRAINT "community_roles_pk" PRIMARY KEY ("role_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "community_user_events" (
	"event_id" integer NOT NULL,
	"community_id" integer NOT NULL,
	"user_id" integer NOT NULL,
	"date" timestamp NOT NULL,
	"status_id" integer NOT NULL,
	"change_role" BOOLEAN NOT NULL,
	"new_role" varchar(50) NOT NULL,
	CONSTRAINT "community_user_events_pk" PRIMARY KEY ("event_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "warnings" (
	"warning_id" integer NOT NULL,
	"type" TEXT NOT NULL,
	"id" integer NOT NULL,
	"name" TEXT NOT NULL,
	"description" TEXT NOT NULL,
	"punishment_id" integer NOT NULL,
	CONSTRAINT "warnings_pk" PRIMARY KEY ("warning_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "courses" (
	"course_id" integer NOT NULL,
	"course_owner_id" integer NOT NULL,
	"users" integer[] NOT NULL,
	"course_owner_type" integer NOT NULL,
	"description" TEXT NOT NULL,
	"level" integer NOT NULL,
	"href" TEXT NOT NULL,
	"conditions" TEXT[] NOT NULL,
	"online" BOOLEAN NOT NULL,
	"create_date" timestamp NOT NULL,
	"warning_id" integer NOT NULL,
	"country_id" integer NOT NULL,
	"city_id" integer NOT NULL,
	"achievements_give" integer[] NOT NULL,
	"free" BOOLEAN NOT NULL,
	"company" TEXT,
	"new" BOOLEAN NOT NULL,
	"sphere" TEXT NOT NULL,
	"assistants" integer[] NOT NULL,
	"duration" integer NOT NULL,
	"course_content" TEXT NOT NULL,
	"final_exam" BOOLEAN NOT NULL,
	"is_individual" BOOLEAN NOT NULL,
	"language" TEXT NOT NULL,
	CONSTRAINT "courses_pk" PRIMARY KEY ("course_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "final_exam" (
	"exam_id" integer NOT NULL,
	"course_id" integer NOT NULL,
	"description" TEXT NOT NULL,
	"online" BOOLEAN NOT NULL,
	"host_exam_id" integer NOT NULL,
	CONSTRAINT "final_exam_pk" PRIMARY KEY ("exam_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "courses_statistics" (
	"course_id" integer NOT NULL,
	"participants" integer NOT NULL,
	"rating" integer NOT NULL,
	"likes" integer NOT NULL,
	"successful_ended" integer NOT NULL,
	"comments" integer NOT NULL,
	"achivements" integer NOT NULL,
	"recommendation" integer NOT NULL,
	CONSTRAINT "courses_statistics_pk" PRIMARY KEY ("course_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "course_calendar" (
	"calendar_id" integer NOT NULL,
	"course_id" integer NOT NULL,
	"from_date" timestamp NOT NULL,
	"to_date" timestamp NOT NULL,
	"type" integer NOT NULL,
	"name" varchar(50) NOT NULL,
	"description" TEXT NOT NULL,
	"class_id" integer[] NOT NULL,
	"user_id" integer[] NOT NULL,
	CONSTRAINT "course_calendar_pk" PRIMARY KEY ("calendar_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "course_classes" (
	"class_id" integer NOT NULL,
	"course_id" integer NOT NULL,
	"users" integer[] NOT NULL,
	"date_create" timestamp NOT NULL,
	"assistants" integer[],
	CONSTRAINT "course_classes_pk" PRIMARY KEY ("class_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "course_class_events" (
	"event_id" integer NOT NULL,
	"class_id" integer NOT NULL,
	"user_id" integer NOT NULL,
	"status_id" integer NOT NULL,
	"date" timestamp NOT NULL,
	CONSTRAINT "course_class_events_pk" PRIMARY KEY ("event_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "recommendations" (
	"recommendation_for_id" integer NOT NULL,
	"users" integer[] NOT NULL,
	"communities" integer[] NOT NULL,
	"courses" integer[] NOT NULL,
	"achievements" integer[] NOT NULL,
	"is_user" BOOLEAN NOT NULL,
	"is_community" BOOLEAN NOT NULL,
	"is_course" BOOLEAN NOT NULL,
	CONSTRAINT "recommendations_pk" PRIMARY KEY ("recommendation_for_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "transactions" (
	"transaction_id" integer NOT NULL,
	"user_sender_id" integer NOT NULL,
	"reciever_id" integer NOT NULL,
	"date" timestamp NOT NULL,
	"transaction_type_id" integer NOT NULL,
	"comment" varchar(50) NOT NULL,
	"service_id" integer NOT NULL,
	"bill_id" integer NOT NULL,
	"is_cancelled" BOOLEAN NOT NULL,
	"for_user" BOOLEAN NOT NULL,
	"for_community" BOOLEAN NOT NULL,
	"for_course" BOOLEAN NOT NULL,
	"payment_value" integer NOT NULL,
	"wallet_id" integer NOT NULL,
	CONSTRAINT "transactions_pk" PRIMARY KEY ("transaction_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "transactions_type" (
	"transaction_type_id" integer NOT NULL,
	"frequency" integer NOT NULL,
	"conditions" varchar(50) NOT NULL,
	"currency" varchar(50) NOT NULL,
	"incognito" varchar(50) NOT NULL,
	CONSTRAINT "transactions_type_pk" PRIMARY KEY ("transaction_type_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "bills" (
	"bill_id" integer NOT NULL,
	"bill_img" TEXT NOT NULL,
	CONSTRAINT "bills_pk" PRIMARY KEY ("bill_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "community_wallet" (
	"wallet_id" integer NOT NULL,
	"value" integer NOT NULL,
	"currency" TEXT NOT NULL,
	"history" JSONB NOT NULL,
	"user_senders" integer[] NOT NULL,
	"responsible_users" integer[] NOT NULL,
	"is_active" BOOLEAN NOT NULL,
	"goal" varchar(50) NOT NULL,
	"community_id" integer NOT NULL,
	CONSTRAINT "community_wallet_pk" PRIMARY KEY ("wallet_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "community_goals" (
	"goal_id" integer NOT NULL,
	"name" varchar(50) NOT NULL,
	"description" TEXT NOT NULL,
	"from_date" timestamp NOT NULL,
	"to_date" timestamp NOT NULL,
	"money_amount" integer NOT NULL,
	"community_id" integer NOT NULL,
	"wallet_id" integer NOT NULL,
	"is_nessesarity" BOOLEAN NOT NULL,
	"user_must_send" integer[] NOT NULL,
	CONSTRAINT "community_goals_pk" PRIMARY KEY ("goal_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "user_goals" (
	"user_goal_id" integer NOT NULL,
	"user_id" integer NOT NULL,
	"name" varchar(50) NOT NULL,
	"description" TEXT NOT NULL,
	"from_date" timestamp NOT NULL,
	"to_date" timestamp NOT NULL,
	"notification_type" varchar NOT NULL,
	"notification_frequency" varchar NOT NULL,
	CONSTRAINT "user_goals_pk" PRIMARY KEY ("user_goal_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "achievements" (
	"achievement_id" integer NOT NULL,
	"user_id" integer NOT NULL,
	"community_id" integer NOT NULL,
	"course_id" integer NOT NULL,
	"name" varchar(50) NOT NULL,
	"description" TEXT NOT NULL,
	"conditions" TEXT[] NOT NULL,
	"country_id" integer NOT NULL,
	"city_id" integer NOT NULL,
	"type" BOOLEAN NOT NULL,
	"grade" varchar NOT NULL,
	"ability" varchar NOT NULL,
	"sphere_id" integer NOT NULL,
	"subsphere_id" integer NOT NULL,
	"online" BOOLEAN NOT NULL,
	"parent_id" integer NOT NULL,
	"image_id" integer NOT NULL,
	"created_date" timestamp NOT NULL,
	"warning_id" integer NOT NULL,
	"global" BOOLEAN NOT NULL,
	"new" BOOLEAN NOT NULL,
	CONSTRAINT "achievements_pk" PRIMARY KEY ("achievement_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "achi_conditions" (
	"condition_id" integer NOT NULL,
	"name" varchar(50) NOT NULL,
	"description" TEXT NOT NULL,
	"from_date" timestamp NOT NULL,
	"to_date" timestamp NOT NULL,
	"parameter" TEXT NOT NULL,
	"value" integer NOT NULL,
	CONSTRAINT "achi_conditions_pk" PRIMARY KEY ("condition_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "spheres" (
	"subsphere_id" integer NOT NULL UNIQUE,
	"sphere_name" varchar(50) NOT NULL,
	"sphere_id" integer NOT NULL UNIQUE,
	"subsphere_name" varchar(50) NOT NULL,
	CONSTRAINT "spheres_pk" PRIMARY KEY ("subsphere_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "punishments" (
	"punishment_id" integer NOT NULL,
	"type" integer NOT NULL,
	"from_date" timestamp NOT NULL,
	"to_date" timestamp NOT NULL,
	"name" varchar(50) NOT NULL,
	"description" TEXT NOT NULL,
	"condition_to_skip" TEXT[] NOT NULL,
	CONSTRAINT "punishments_pk" PRIMARY KEY ("punishment_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "achi_statistics" (
	"achievement_id" integer NOT NULL,
	"likes" integer NOT NULL,
	"reccomended" integer NOT NULL,
	"frequency_get" integer NOT NULL,
	"frequency_in_plan" integer NOT NULL,
	CONSTRAINT "achi_statistics_pk" PRIMARY KEY ("achievement_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "tasks" (
	"task_id" integer NOT NULL,
	"user_id" integer NOT NULL,
	"community_id" integer NOT NULL,
	"course_id" integer NOT NULL,
	"file_path" TEXT NOT NULL,
	"questions" TEXT[] NOT NULL,
	"answers" TEXT[] NOT NULL,
	"pass_percent" integer NOT NULL,
	CONSTRAINT "tasks_pk" PRIMARY KEY ("task_id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "status" (
	"status_id" integer NOT NULL,
	"description" varchar(19) NOT NULL,
	CONSTRAINT "status_pk" PRIMARY KEY ("status_id")
) WITH (
  OIDS=FALSE
);



ALTER TABLE "authentication" ADD CONSTRAINT "authentication_fk0" FOREIGN KEY ("email") REFERENCES "users_main"("email");
ALTER TABLE "authentication" ADD CONSTRAINT "authentication_fk1" FOREIGN KEY ("phone") REFERENCES "users_main"("phone");


ALTER TABLE "users_information" ADD CONSTRAINT "users_information_fk0" FOREIGN KEY ("user_id") REFERENCES "users_main"("user_id");

ALTER TABLE "user_statistics" ADD CONSTRAINT "user_statistics_fk0" FOREIGN KEY ("user_id") REFERENCES "users_information"("user_id");

ALTER TABLE "user_calendar" ADD CONSTRAINT "user_calendar_fk0" FOREIGN KEY ("user_id") REFERENCES "users_information"("user_id");

ALTER TABLE "friends" ADD CONSTRAINT "friends_fk0" FOREIGN KEY ("user_id") REFERENCES "users_information"("user_id");

ALTER TABLE "friend_events" ADD CONSTRAINT "friend_events_fk0" FOREIGN KEY ("relationship_id") REFERENCES "friends"("relationship_id");
ALTER TABLE "friend_events" ADD CONSTRAINT "friend_events_fk1" FOREIGN KEY ("user_id_1") REFERENCES "friends"("user_id");
ALTER TABLE "friend_events" ADD CONSTRAINT "friend_events_fk2" FOREIGN KEY ("user_id_2") REFERENCES "friends"("user_id");
ALTER TABLE "friend_events" ADD CONSTRAINT "friend_events_fk3" FOREIGN KEY ("status_id") REFERENCES "status"("status_id");

ALTER TABLE "sessions" ADD CONSTRAINT "sessions_fk0" FOREIGN KEY ("user_id") REFERENCES "users_main"("user_id");



ALTER TABLE "cities" ADD CONSTRAINT "cities_fk0" FOREIGN KEY ("country_id") REFERENCES "countries"("country_id");

ALTER TABLE "communities" ADD CONSTRAINT "communities_fk0" FOREIGN KEY ("country_id") REFERENCES "countries"("country_id");
ALTER TABLE "communities" ADD CONSTRAINT "communities_fk1" FOREIGN KEY ("city_id") REFERENCES "cities"("city_id");
ALTER TABLE "communities" ADD CONSTRAINT "communities_fk2" FOREIGN KEY ("image_id") REFERENCES "images"("image_id");

ALTER TABLE "community_meetings" ADD CONSTRAINT "community_meetings_fk0" FOREIGN KEY ("community_id") REFERENCES "communities"("community_id");
ALTER TABLE "community_meetings" ADD CONSTRAINT "community_meetings_fk1" FOREIGN KEY ("meeting_image_id") REFERENCES "images"("image_id");

ALTER TABLE "community_conditions" ADD CONSTRAINT "community_conditions_fk0" FOREIGN KEY ("community_id") REFERENCES "communities"("community_id");

ALTER TABLE "community_statistics" ADD CONSTRAINT "community_statistics_fk0" FOREIGN KEY ("community_id") REFERENCES "communities"("community_id");

ALTER TABLE "community_roles" ADD CONSTRAINT "community_roles_fk0" FOREIGN KEY ("community_id") REFERENCES "communities"("community_id");

ALTER TABLE "community_user_events" ADD CONSTRAINT "community_user_events_fk0" FOREIGN KEY ("community_id") REFERENCES "communities"("community_id");
ALTER TABLE "community_user_events" ADD CONSTRAINT "community_user_events_fk1" FOREIGN KEY ("user_id") REFERENCES "users_information"("user_id");
ALTER TABLE "community_user_events" ADD CONSTRAINT "community_user_events_fk2" FOREIGN KEY ("status_id") REFERENCES "status"("status_id");

ALTER TABLE "warnings" ADD CONSTRAINT "warnings_fk0" FOREIGN KEY ("punishment_id") REFERENCES "punishments"("punishment_id");

ALTER TABLE "courses" ADD CONSTRAINT "courses_fk1" FOREIGN KEY ("warning_id") REFERENCES "warnings"("warning_id");

ALTER TABLE "final_exam" ADD CONSTRAINT "final_exam_fk0" FOREIGN KEY ("course_id") REFERENCES "courses"("course_id");

ALTER TABLE "courses_statistics" ADD CONSTRAINT "courses_statistics_fk0" FOREIGN KEY ("course_id") REFERENCES "courses"("course_id");

ALTER TABLE "course_calendar" ADD CONSTRAINT "course_calendar_fk0" FOREIGN KEY ("course_id") REFERENCES "courses"("course_id");

ALTER TABLE "course_classes" ADD CONSTRAINT "course_classes_fk0" FOREIGN KEY ("course_id") REFERENCES "courses"("course_id");

ALTER TABLE "course_class_events" ADD CONSTRAINT "course_class_events_fk0" FOREIGN KEY ("class_id") REFERENCES "course_classes"("class_id");
ALTER TABLE "course_class_events" ADD CONSTRAINT "course_class_events_fk1" FOREIGN KEY ("user_id") REFERENCES "users_main"("user_id");
ALTER TABLE "course_class_events" ADD CONSTRAINT "course_class_events_fk2" FOREIGN KEY ("status_id") REFERENCES "status"("status_id");


ALTER TABLE "transactions" ADD CONSTRAINT "transactions_fk0" FOREIGN KEY ("transaction_type_id") REFERENCES "transactions_type"("transaction_type_id");
ALTER TABLE "transactions" ADD CONSTRAINT "transactions_fk1" FOREIGN KEY ("bill_id") REFERENCES "bills"("bill_id");
ALTER TABLE "transactions" ADD CONSTRAINT "transactions_fk2" FOREIGN KEY ("wallet_id") REFERENCES "community_wallet"("wallet_id");



ALTER TABLE "community_wallet" ADD CONSTRAINT "community_wallet_fk0" FOREIGN KEY ("community_id") REFERENCES "communities"("community_id");

ALTER TABLE "community_goals" ADD CONSTRAINT "community_goals_fk0" FOREIGN KEY ("community_id") REFERENCES "communities"("community_id");
ALTER TABLE "community_goals" ADD CONSTRAINT "community_goals_fk1" FOREIGN KEY ("wallet_id") REFERENCES "community_wallet"("wallet_id");

ALTER TABLE "user_goals" ADD CONSTRAINT "user_goals_fk0" FOREIGN KEY ("user_id") REFERENCES "users_main"("user_id");

ALTER TABLE "achievements" ADD CONSTRAINT "achievements_fk0" FOREIGN KEY ("user_id") REFERENCES "users_main"("user_id");
ALTER TABLE "achievements" ADD CONSTRAINT "achievements_fk1" FOREIGN KEY ("community_id") REFERENCES "communities"("community_id");
ALTER TABLE "achievements" ADD CONSTRAINT "achievements_fk2" FOREIGN KEY ("course_id") REFERENCES "courses"("course_id");
ALTER TABLE "achievements" ADD CONSTRAINT "achievements_fk3" FOREIGN KEY ("country_id") REFERENCES "countries"("country_id");
ALTER TABLE "achievements" ADD CONSTRAINT "achievements_fk4" FOREIGN KEY ("city_id") REFERENCES "cities"("city_id");
ALTER TABLE "achievements" ADD CONSTRAINT "achievements_fk5" FOREIGN KEY ("sphere_id") REFERENCES "spheres"("sphere_id");
ALTER TABLE "achievements" ADD CONSTRAINT "achievements_fk6" FOREIGN KEY ("subsphere_id") REFERENCES "spheres"("subsphere_id");
ALTER TABLE "achievements" ADD CONSTRAINT "achievements_fk7" FOREIGN KEY ("image_id") REFERENCES "images"("image_id");
ALTER TABLE "achievements" ADD CONSTRAINT "achievements_fk8" FOREIGN KEY ("warning_id") REFERENCES "warnings"("warning_id");




ALTER TABLE "achi_statistics" ADD CONSTRAINT "achi_statistics_fk0" FOREIGN KEY ("achievement_id") REFERENCES "achievements"("achievement_id");

ALTER TABLE "tasks" ADD CONSTRAINT "tasks_fk0" FOREIGN KEY ("user_id") REFERENCES "users_main"("user_id");
ALTER TABLE "tasks" ADD CONSTRAINT "tasks_fk1" FOREIGN KEY ("community_id") REFERENCES "communities"("community_id");
ALTER TABLE "tasks" ADD CONSTRAINT "tasks_fk2" FOREIGN KEY ("course_id") REFERENCES "courses"("course_id");









































""")
