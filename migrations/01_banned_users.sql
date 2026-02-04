-- Create table for banned users
create table if not exists banned_users (
  id uuid default gen_random_uuid() primary key,
  email text unique not null,
  reason text,
  banned_at timestamptz default now(),
  banned_by uuid references auth.users(id)
);

-- Enable RLS
alter table banned_users enable row level security;

-- Policies
-- Only admins (via service role or if we had an admin role) can insert/delete
-- For MVP, we use service_role for admin actions, so we might not need complicated policies if using supabase_admin client.
-- However, 'base.py' needs to READ this table to check for bans.
-- We can allow public read for now or authenticated read, or preferably restrict it.
-- Let's allow authenticated read so any logged in user can check if they are banned (or rather the app can check).
-- Ideally, we'd use a secure function, but a select policy is easier.

create policy "Enable read access for all users" on banned_users for select using (true);

-- Allow full access to service_role (implicit, but good to note)
