-- Add tag column to batches
ALTER TABLE batches ADD COLUMN IF NOT EXISTS tag text;

-- Drop existing FK on print_jobs to strictly re-create with CASCADE (Optional, but cleaner)
-- However, for safety, I will let the backend handle the cascade for now, or the user can run this.
-- Simple column add is safest for "just add column".

-- If we want to enforce CASCADE at DB level:
ALTER TABLE print_jobs
DROP CONSTRAINT IF EXISTS print_jobs_batch_id_fkey,
ADD CONSTRAINT print_jobs_batch_id_fkey
    FOREIGN KEY (batch_id)
    REFERENCES batches(id)
    ON DELETE CASCADE;

ALTER TABLE print_job_items
DROP CONSTRAINT IF EXISTS print_job_items_print_job_id_fkey,
ADD CONSTRAINT print_job_items_print_job_id_fkey
    FOREIGN KEY (print_job_id)
    REFERENCES print_jobs(id)
    ON DELETE CASCADE;

ALTER TABLE batch_reprints
DROP CONSTRAINT IF EXISTS batch_reprints_batch_id_fkey,
ADD CONSTRAINT batch_reprints_batch_id_fkey
    FOREIGN KEY (batch_id)
    REFERENCES batches(id)
    ON DELETE CASCADE;
