import uvicorn
import sys
from pathlib import Path

# Add project root to sys.path to resolve backend imports cleanly
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    print("[BACKEND] Starting FastAPI Server on http://localhost:8000...")
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
