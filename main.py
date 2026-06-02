import os
import sys

# Force absolute path resolution of project root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)

# ================= DIAGNOSTICS & CASE-SENSITIVITY RESOLVER =================
print("================= RENDER DEPLOY DIAGNOSTICS =================")
print(f"Current Working Directory: {os.getcwd()}")
print(f"ROOT_DIR resolved to: {ROOT_DIR}")
try:
    items = os.listdir(ROOT_DIR)
    print(f"Files/Folders at root: {items}")
except Exception as e:
    print(f"Failed to list ROOT_DIR: {e}")
    items = []

for target in ["backend", "frontend"]:
    found_target = False
    for name in items:
        if name.lower() == target:
            found_target = True
            target_path = os.path.join(ROOT_DIR, name)
            print(f"-> Found folder/file matching '{target}': '{name}'")
            
            # Dynamic case-sensitivity renaming if mismatched
            if name != target:
                new_path = os.path.join(ROOT_DIR, target)
                try:
                    os.rename(target_path, new_path)
                    print(f"   Dynamically renamed '{name}' to '{target}' to resolve case-sensitivity.")
                    target_path = new_path
                except Exception as rename_e:
                    print(f"   Failed to rename '{name}' to '{target}': {rename_e}")
            
            if os.path.isdir(target_path):
                try:
                    print(f"   Contents of '{target}': {os.listdir(target_path)}")
                except Exception as list_e:
                    print(f"   Failed to list contents of '{target}': {list_e}")
            else:
                print(f"   WARNING: '{target}' is NOT a directory!")
                
    if not found_target:
        print(f"-> ERROR: No file or folder named '{target}' (case-insensitive) was found at root!")
print("=============================================================")



from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.database import engine, get_db_status, Base
from backend.schemas import DatabaseStatusResponse

# Import Decoupled Face Analyzer Modules
from backend import scanner
from backend import history
from backend import analytics

# Initialize FastAPI Root Application
app = FastAPI(
    title="AI Face Analyzer - Main Application Suite",
    description="Decoupled Modular Enterprise Suite for Computer Vision Face Scanning & Analytics.",
    version="3.0.0"
)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Storage Folders in Root (for uploads and scans)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(ROOT_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount Image static server
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Dynamic DB Initializer
@app.on_event("startup")
def startup_event():
    try:
        Base.metadata.create_all(bind=engine)
        print("Face analysis database tables initialized successfully.")
    except Exception as e:
        print(f"Error during database schema initialization: {e}")

# Register APIRouters
app.include_router(scanner.router)
app.include_router(history.router)
app.include_router(analytics.router)

# Real-time Active Visitor Tracker State
ACTIVE_VISITORS = {}  # client_id -> last_seen_timestamp

@app.post("/api/visitor/heartbeat")
def visitor_heartbeat(client_id: str = Query(...)):
    """Receives a heartbeat ping from an active frontend client."""
    import time
    ACTIVE_VISITORS[client_id] = time.time()
    return {"status": "ok"}

@app.get("/api/admin/active-visitors")
def get_active_visitors(secret: str = Query(None)):
    """Gets the count of active visitors. Protected by a simple secret key."""
    import time
    now = time.time()
    # Clean up expired visitor sessions (older than 25 seconds)
    expired = [cid for cid, t in ACTIVE_VISITORS.items() if now - t > 25]
    for cid in expired:
        ACTIVE_VISITORS.pop(cid, None)
        
    # Secret protection check
    if secret != "xai_admin_secret_99":
        raise HTTPException(status_code=403, detail="Unauthorized")
        
    return {"active_count": len(ACTIVE_VISITORS)}


# Expose global DB status check
@app.get("/api/db-status", response_model=DatabaseStatusResponse)
def db_status():
    """Get status of active PostgreSQL database / SQLite fallback."""
    return get_db_status()



# ==========================================================================
# MULTI-PAGE FRONTEND ROUTER (HTML WEB LINKS)
# ==========================================================================

FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

@app.get("/")
@app.get("/scanner")
def serve_scanner():
    """Serves the main interactive Face Scanner HTML dashboard."""
    index_path = os.path.join(FRONTEND_DIR, "scanner.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Scanner UI module not found inside frontend/ directory."}

@app.get("/history")
def serve_history():
    """Serves the History logs list HTML module."""
    index_path = os.path.join(FRONTEND_DIR, "history.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "History UI module not found inside frontend/ directory."}

@app.get("/analytics")
def serve_analytics():
    """Serves the Chart.js visual statistics HTML module."""
    index_path = os.path.join(FRONTEND_DIR, "analytics.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Analytics UI module not found inside frontend/ directory."}
