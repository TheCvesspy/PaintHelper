
path = 'd:/PaintHelper/PaintHelper/minipaint/pages/dashboard.py'
try:
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    start_idx = 1325 # Line 1326
    
    end_idx = -1
    for i, line in enumerate(lines):
        if i > start_idx and "def recipes_tab():" in line:
            end_idx = i
            break
            
    if end_idx != -1:
        print(f"Deleting from {start_idx} (Line {start_idx+1}) to {end_idx} (Line {end_idx+1})")
        print(f"Content start: {lines[start_idx]}")
        print(f"Content end marker: {lines[end_idx]}")
        
        del lines[start_idx:end_idx]
        
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print("Success.")
    else:
        print("Could not find end marker 'def recipes_tab():'")

except Exception as e:
    print(f"Error: {e}")
