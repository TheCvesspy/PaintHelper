from pydantic import BaseModel


class BatchReprint(BaseModel):
    """Represents a reprint request for failed prints"""
    id: str
    batch_id: str
    name: str
    quantity: int
    created_at: str


class PrintJobItem(BaseModel):
    """Represents a single item in a print job"""
    id: str
    print_job_id: str
    name: str
    link_url: str = ""  # Enforce string, default empty
    quantity: int


class PrintJob(BaseModel):
    """Represents a print job with multiple items"""
    id: str
    batch_id: str
    name: str | None
    status: str
    progress_percent: int
    started_at: str | None
    print_job_items: list[PrintJobItem]
    display_number: int = 0


class Batch(BaseModel):
    """Represents a batch of print jobs"""
    id: str
    user_id: str
    name: str
    tag: str | None  # FDM, Resin, etc
    due_date: str | None
    is_archived: bool
    created_at: str
    print_jobs: list[PrintJob]
    batch_reprints: list[BatchReprint]
    progress: int = 0
