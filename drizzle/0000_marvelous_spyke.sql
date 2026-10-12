CREATE TABLE `membership` (
	`id` text PRIMARY KEY NOT NULL,
	`role` text NOT NULL,
	`student_id` text
);
--> statement-breakpoint
CREATE TABLE `portal_state` (
	`id` text PRIMARY KEY NOT NULL,
	`payload` text NOT NULL,
	`revision` integer DEFAULT 0 NOT NULL
);
--> statement-breakpoint
CREATE TABLE `sessions` (
	`id` text PRIMARY KEY NOT NULL,
	`user_id` text NOT NULL,
	`role` text NOT NULL,
	`student_id` text,
	`expires` integer NOT NULL
);
