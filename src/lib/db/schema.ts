import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";

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
