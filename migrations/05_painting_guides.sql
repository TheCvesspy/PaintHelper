-- Migration: 05_painting_guides.sql
-- Description: Replaces recipes table with painting_guides, guide_details, and guide_paints tables.

-- 1. Drop old recipes table
drop table if exists public.recipes;

-- 2. Create painting_guides table
create table public.painting_guides (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references auth.users not null,
    name text not null,
    note text,
    image_drive_id text, -- ID of file in Google Drive
    created_at timestamp with time zone default now()
);

-- RLS
alter table public.painting_guides enable row level security;
create policy "Users see their own guides"
on public.painting_guides for all
using (auth.uid() = user_id);

-- 3. Create guide_details table
create table public.guide_details (
    id uuid primary key default uuid_generate_v4(),
    guide_id uuid references public.painting_guides(id) on delete cascade not null,
    name text not null, -- e.g. "Cape", "Armor"
    order_index int default 0,
    created_at timestamp with time zone default now()
);

-- RLS
alter table public.guide_details enable row level security;
create policy "Users manage their own guide details"
on public.guide_details for all
using (
    exists (
        select 1 from public.painting_guides
        where public.painting_guides.id = guide_details.guide_id
        and public.painting_guides.user_id = auth.uid()
    )
);

-- 4. Create guide_paints table
create table public.guide_paints (
    id uuid primary key default uuid_generate_v4(),
    detail_id uuid references public.guide_details(id) on delete cascade not null,
    paint_name text not null, -- We store name to be robust against library changes
    paint_color_hex text,     -- Snapshot of color
    paint_id uuid,            -- Optional link to catalog_paints or user_paints if we want to track
    ratio int default 1,      -- e.g. 2 means "2 parts"
    note text,                -- Optional specific note for this paint usage
    order_index int default 0,
    created_at timestamp with time zone default now()
);

-- RLS
alter table public.guide_paints enable row level security;
create policy "Users manage their own guide paints"
on public.guide_paints for all
using (
    exists (
        select 1 from public.guide_details
        join public.painting_guides on public.painting_guides.id = public.guide_details.guide_id
        where public.guide_details.id = guide_paints.detail_id
        and public.painting_guides.user_id = auth.uid()
    )
);
