CREATE TABLE `reddit_mentions` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`term` text NOT NULL,
	`post_id` text NOT NULL,
	`title` text NOT NULL,
	`url` text NOT NULL,
	`subreddit` text NOT NULL,
	`score` integer DEFAULT 0 NOT NULL,
	`num_comments` integer DEFAULT 0 NOT NULL,
	`created_utc` integer NOT NULL,
	`over_18` integer DEFAULT false NOT NULL,
	`synced_at` text NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `reddit_mentions_post_id` ON `reddit_mentions` (`post_id`);--> statement-breakpoint
CREATE TABLE `reddit_tracked_terms` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`term` text NOT NULL,
	`created_at` text NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `reddit_tracked_terms_term_unique` ON `reddit_tracked_terms` (`term`);