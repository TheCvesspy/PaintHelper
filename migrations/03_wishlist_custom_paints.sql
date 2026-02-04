-- Add custom_paint_id to paint_wishlist table
alter table public.paint_wishlist 
add column custom_paint_id uuid references public.custom_paints(id);

-- Constraint to ensure we don't duplicate items (either same paint_id OR same custom_paint_id for user)
-- Note: existing unique constraint is likely on (user_id, paint_id). 
-- We might need a check constraint that at least one is set, but keeping it simple for now.
-- Ideally we would have a unique partial index or just rely on application logic + unique constraint on (user_id, custom_paint_id).

create unique index unique_user_custom_wishlist on public.paint_wishlist (user_id, custom_paint_id) where custom_paint_id is not null;
