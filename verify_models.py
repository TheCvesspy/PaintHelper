import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from minipaint.models.guide import PaintingGuide, GuideDetail, GuidePaint

try:
    print("Testing GuidePaint model with new 'role' field...")
    paint = GuidePaint(
        paint_name="Contrast Paint",
        paint_color_hex="#000000",
        role="contrast",
        note="Apply generic note",
        order_index=0
    )
    print(f"✅ GuidePaint created: {paint}")

    print("\nTesting PaintingGuide model with new fields...")
    guide = PaintingGuide(
        id="123e4567-e89b-12d3-a456-426614174000",
        user_id="123e4567-e89b-12d3-a456-426614174000",
        name="Test Guide",
        guide_type="contrast",
        primer_paint_id="123e4567-e89b-12d3-a456-426614174001",
        is_slapchop=True,
        slapchop_note="Drybrush check",
        is_airbrush=True,
        guide_details=[]
    )
    print(f"✅ PaintingGuide created: {guide}")
    
    # Test nesting
    detail = GuideDetail(id="123", guide_id=guide.id, name="Skin", guide_paints=[paint])
    guide.guide_details = [detail]
    print(f"✅ Nested Guide created successfully.")

except Exception as e:
    print(f"❌ Error verifying models: {e}")
    sys.exit(1)
