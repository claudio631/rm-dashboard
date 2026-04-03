CREATE TABLE `reddit_ad_performance` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`campaign_id` text NOT NULL,
	`date` text NOT NULL,
	`impressions` integer DEFAULT 0 NOT NULL,
	`clicks` integer DEFAULT 0 NOT NULL,
	`spend` integer DEFAULT 0 NOT NULL,
	`conversions` integer DEFAULT 0 NOT NULL,
	`ctr` text,
	`ecpc` integer,
	`ecpa` integer,
	`synced_at` text NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `reddit_ad_perf_campaign_date` ON `reddit_ad_performance` (`campaign_id`,`date`);--> statement-breakpoint
CREATE TABLE `reddit_campaigns` (
	`id` text PRIMARY KEY NOT NULL,
	`name` text NOT NULL,
	`status` text NOT NULL,
	`objective` text,
	`daily_budget_amount` integer,
	`currency` text,
	`synced_at` text NOT NULL
);
