import {sqliteTable,text,integer} from 'drizzle-orm/sqlite-core';
export const portalState=sqliteTable('portal_state',{id:text('id').primaryKey(),payload:text('payload').notNull(),revision:integer('revision').notNull().default(0)});
export const membership=sqliteTable('membership',{id:text('id').primaryKey(),role:text('role').notNull(),studentId:text('student_id')});
export const sessions=sqliteTable('sessions',{id:text('id').primaryKey(),userId:text('user_id').notNull(),role:text('role').notNull(),studentId:text('student_id'),expires:integer('expires').notNull()});
