import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from minipaint.minipaint import app

print("--- Inspecting Routes ---")
if hasattr(app, "_api"):
    starlette_app = app._api
    print(f"Starlette App: {starlette_app}")
    for route in starlette_app.routes:
        print(f"Route: {route.path} -> {route.name}")
else:
    print("No _api attribute found on app.")
print("--- End Inspection ---")
