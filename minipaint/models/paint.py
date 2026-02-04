from typing import TypedDict, Optional


class PaintSetDict(TypedDict):
    """Paint set information"""
    name: str


class BrandDict(TypedDict):
    """Paint brand information"""
    name: str


class PaintDict(TypedDict):
    """Catalog paint information"""
    id: str
    name: str
    product_code: str
    color_hex: str
    paint_sets: Optional[PaintSetDict]
    paint_brands: Optional[BrandDict]


class OwnedPaintDict(TypedDict):
    """User's owned paint from catalog"""
    id: str
    paint_id: str
    catalog_paints: PaintDict


class CustomPaintDict(TypedDict):
    """User's custom paint"""
    id: str
    name: str
    brand_name: str
    set_name: str
    product_code: str
    color_hex: str
    created_at: str


class WishlistPaintDict(TypedDict):
    """Paint on user's wishlist"""
    id: str
    paint_id: Optional[str]
    custom_paint_id: Optional[str]
    catalog_paints: Optional[PaintDict]
    custom_paints: Optional[CustomPaintDict]
