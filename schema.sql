-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- 1. ACCESS TOKENS TABLE
-- Stores invite tokens. Only Admin can insert/view all.
create table public.access_tokens (
    id uuid primary key default uuid_generate_v4(),
    token_code uuid unique default uuid_generate_v4(), -- The actual code user types in
    status text not null check (status in ('active', 'used', 'revoked')) default 'active',
    created_at timestamp with time zone default now(),
    used_at timestamp with time zone,
    used_by_email text -- Store email of who used it
);

-- RLS: Admin only
alter table public.access_tokens enable row level security;

-- NOTE: Replace 'YOUR_ADMIN_EMAIL@gmail.com' with the actual admin email before running
create policy "Admins can do everything on tokens"
on public.access_tokens
for all
using (auth.jwt() ->> 'email' = 'cvesspy@gmail.com'); 

-- 2. USER PREFERENCES / DRIVES
create table public.user_settings (
    user_id uuid references auth.users not null primary key,
    drive_refresh_token text, -- Encrypted? Ideally. For MVP, store as text or use Supabase Vault.
    drive_folder_id text -- ID of the 'MiniPaintTracker' folder in their drive
);

alter table public.user_settings enable row level security;
create policy "Users manage their own settings"
on public.user_settings
for all
using (auth.uid() = user_id);

-- 3. PAINTS
create table public.paints (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references auth.users not null,
    name text not null,
    brand text,
    color_hex text,
    label_image_drive_id text, -- ID of file in Google Drive
    created_at timestamp with time zone default now()
);

alter table public.paints enable row level security;
create policy "Users see their own paints"
on public.paints
for all
using (auth.uid() = user_id);

-- 4. PROJECTS (Miniatures)
create table public.projects (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references auth.users not null,
    name text not null,
    status text default 'planned', -- planned, printed, primed, painting, finished
    description text,
    created_at timestamp with time zone default now()
);

alter table public.projects enable row level security;
create policy "Users see their own projects"
on public.projects
for all
using (auth.uid() = user_id);

-- 5. PRINT JOBS
create table public.print_jobs (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references auth.users not null,
    project_id uuid references public.projects,
    filename text,
    status text default 'printing', -- printing, success, failed
    progress_percent int default 0,
    started_at timestamp with time zone default now()
);

alter table public.print_jobs enable row level security;
create policy "Users see their own print jobs"
on public.print_jobs
for all
using (auth.uid() = user_id);

-- 6. RECIPES (Paint Mixes)
create table public.recipes (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references auth.users not null,
    project_id uuid references public.projects, -- Optional link to project
    name text not null,
    description text, -- "2 parts Blue, 1 part Gray"
    created_at timestamp with time zone default now()
);

alter table public.recipes enable row level security;
create policy "Users see their own recipes"
on public.recipes
for all
using (auth.uid() = user_id);

-- 8. PAINTING GUIDES
create table public.painting_guides (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references auth.users not null,
    name text not null,
    note text,
    guide_type text default 'layering', -- 'layering' or 'contrast'
    primer_paint_id uuid references public.paints, -- Optional primer
    is_airbrush boolean default false,
    is_slapchop boolean default false,
    slapchop_note text,
    image_drive_id text,
    created_at timestamp with time zone default now()
);

alter table public.painting_guides enable row level security;
create policy "Users see their own guides"
on public.painting_guides
for all
using (auth.uid() = user_id);

-- 9. GUIDE DETAILS (Steps/Parts)
create table public.guide_details (
    id uuid primary key default uuid_generate_v4(),
    guide_id uuid references public.painting_guides not null,
    name text not null, -- "Armor", "Skin"
    category text, -- Deprecated in favor of guide_type + specific paints? Or kept for grouping? Kept for "Part Name"
    order_index int default 0,
    created_at timestamp with time zone default now()
);

alter table public.guide_details enable row level security;
create policy "Users see their own guide details"
on public.guide_details
for all
using (
    exists (
        select 1 from public.painting_guides
        where painting_guides.id = guide_details.guide_id
        and painting_guides.user_id = auth.uid()
    )
);

-- 10. GUIDE PAINTS (Specific paints in a step)
create table public.guide_paints (
    id uuid primary key default uuid_generate_v4(),
    detail_id uuid references public.guide_details not null,
    paint_name text not null, -- Snapshot name
    paint_color_hex text, -- Snapshot color
    paint_id uuid references public.paints, -- Link to owned paint (optional)
    role text, -- 'base', 'midtone', 'highlight', 'contrast', 'shade', etc.
    ratio int default 1,
    note text,
    order_index int default 0,
    created_at timestamp with time zone default now()
);

alter table public.guide_paints enable row level security;
create policy "Users see their own guide paints"
on public.guide_paints
for all
using (
    exists (
        select 1 from public.guide_details
        join public.painting_guides on guide_details.guide_id = painting_guides.id
        where guide_details.id = guide_paints.detail_id
        and painting_guides.user_id = auth.uid()
    )
);
