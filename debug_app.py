import reflex as rx
import importlib.metadata

try:
    version = importlib.metadata.version("reflex")
    print(f"Reflex version (metadata): {version}")
except Exception as e:
    print(f"Could not get version: {e}")

try:
    print(f"Reflex file: {rx.__file__}")
except:
    pass

app = rx.App()

print("\n--- App Public Attributes ---")
for attr in dir(app):
    if not attr.startswith("_"):
        print(attr)

# Check router
if hasattr(app, "router"):
    val = getattr(app, "router")
    print(f"\nFOUND 'router': {type(val)}")
    print("Router dir:", [x for x in dir(val) if not x.startswith("_")])
