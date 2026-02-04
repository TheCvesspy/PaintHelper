from pydantic import BaseModel


class GuidePaint(BaseModel):
    """Represents a paint used in a painting guide detail"""
    id: str = ""
    detail_id: str = ""
    paint_name: str
    paint_color_hex: str
    paint_id: str | None = None
    role: str | None = None  # Base, Midtone, Highlight, etc.
    ratio: int = 1
    note: str | None = None
    order_index: int = 0


class GuideDetail(BaseModel):
    """Represents a detail/step in a painting guide"""
    id: str = ""
    guide_id: str = ""
    name: str
    description: str | None = None
    category: str | None = None  # Basecoat, Layer, Highlight, Drybrush, Shading, Wash
    order_index: int = 0
    guide_paints: list[GuidePaint] = []  # Nested paints
    layer_roles: list[str] = ["layer_0"] # For UI state: list of active layer roles
    is_collapsed: bool = False # For UI state: toggle visibility of paints


class PaintingGuide(BaseModel):
    """Represents a complete painting guide"""
    id: str = ""
    user_id: str = ""
    name: str
    note: str | None = None
    guide_type: str = "layering"  # 'layering' or 'contrast'
    primer_paint_id: str | None = None
    is_airbrush: bool = False
    is_slapchop: bool = False
    slapchop_note: str | None = None
    image_drive_id: str | None = None
    created_at: str = ""
    guide_details: list[GuideDetail] = []
