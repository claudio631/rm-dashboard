import { sqliteTable, text, integer, uniqueIndex } from "drizzle-orm/sqlite-core";

export const redditTokens = sqliteTable("reddit_tokens", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  accessToken: text("access_token").notNull(),
  refreshToken: text("refresh_token").notNull(),
  expiresAt: text("expires_at").notNull(),
  scope: text("scope").notNull(),
  createdAt: text("created_at")
    .notNull()
    .$defaultFn(() => new Date().toISOString()),
  updatedAt: text("updated_at")
    .notNull()
    .$defaultFn(() => new Date().toISOString()),
});

export const redditCampaigns = sqliteTable("reddit_campaigns", {
  id: text("id").primaryKey(), // Reddit campaign ID (e.g. "2393827658041853846")
  name: text("name").notNull(),
  status: text("status").notNull(),
  objective: text("objective"),
  dailyBudgetAmount: integer("daily_budget_amount"), // microcurrency
  currency: text("currency"),
  syncedAt: text("synced_at").notNull(),
});

export const redditAdPerformance = sqliteTable(
  "reddit_ad_performance",
  {
    id: integer("id").primaryKey({ autoIncrement: true }),
    campaignId: text("campaign_id").notNull(),
    date: text("date").notNull(), // "YYYY-MM-DD"
    impressions: integer("impressions").notNull().default(0),
    clicks: integer("clicks").notNull().default(0),
    spend: integer("spend").notNull().default(0), // microcurrency
    conversions: integer("conversions").notNull().default(0),
    ctr: text("ctr"), // computed: clicks/impressions as decimal string
    ecpc: integer("ecpc"), // microcurrency
    ecpa: integer("ecpa"), // microcurrency
    syncedAt: text("synced_at").notNull(),
  },
  (table) => [uniqueIndex("reddit_ad_perf_campaign_date").on(table.campaignId, table.date)]
);

export const uploads = sqliteTable("uploads", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  filename: text("filename").notNull(),
  fileType: text("file_type").notNull(),
  uploadedAt: text("uploaded_at")
    .notNull()
    .$defaultFn(() => new Date().toISOString()),
  rowCount: integer("row_count"),
  status: text("status").notNull().default("pending"),
});
