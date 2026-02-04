-- Migration: Add category field to guide_details
-- Purpose: Allow categorization of painting steps (Basecoat, Layer, Highlight, etc.)

alter table public.guide_details 
add column category text;

alter table public.guide_details
add constraint category_check 
check (category in ('Basecoat', 'Layer', 'Highlight', 'Drybrush', 'Shading', 'Wash'));

-- Add default category for existing records
update public.guide_details 
set category = 'Layer' 
where category is null;
