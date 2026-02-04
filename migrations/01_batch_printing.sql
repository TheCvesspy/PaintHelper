-- Batch Printing Schema

-- 1. Batches Table
create table public.batches (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references auth.users not null,
    name text not null,
    due_date date,
    is_archived boolean default false,
    created_at timestamp with time zone default now()
);

alter table public.batches enable row level security;
create policy "Users see their own batches"
on public.batches for all
using (auth.uid() = user_id);

-- 2. Modify Print Jobs (Add batch_id, name)
alter table public.print_jobs
add column batch_id uuid references public.batches,
add column name text;

-- 3. Print Job Items (for granular tracking)
create table public.print_job_items (
    id uuid primary key default uuid_generate_v4(),
    print_job_id uuid references public.print_jobs not null,
    name text not null,
    link_url text, -- Voluntary link
    quantity int default 1
);

alter table public.print_job_items enable row level security;
create policy "Users see their own print job items"
on public.print_job_items for all
using (
    exists (
        select 1 from public.print_jobs
        where print_jobs.id = print_job_items.print_job_id
        and print_jobs.user_id = auth.uid()
    )
);

-- 4. Batch Reprints (for failed items)
create table public.batch_reprints (
    id uuid primary key default uuid_generate_v4(),
    batch_id uuid references public.batches not null,
    name text not null,
    quantity int default 1,
    created_at timestamp with time zone default now()
);

alter table public.batch_reprints enable row level security;
create policy "Users see their own batch reprints"
on public.batch_reprints for all
using (
    exists (
        select 1 from public.batches
        where batches.id = batch_reprints.batch_id
        and batches.user_id = auth.uid()
    )
);
