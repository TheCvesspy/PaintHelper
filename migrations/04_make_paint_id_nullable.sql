-- Make paint_id nullable to support custom paints in wishlist
alter table public.paint_wishlist 
alter column paint_id drop not null;

-- Optional: Add check constraint to ensure at least one ID is present
-- alter table public.paint_wishlist 
-- add constraint check_paint_or_custom check (paint_id is not null or custom_paint_id is not null);
