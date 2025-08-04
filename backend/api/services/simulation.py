from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.note import Note
from api.database import get_db
from typing import Dict, Any
import time
import random
import asyncio
from datetime import datetime

router = APIRouter(prefix="/simulation", tags=["simulation"])

@router.get("/slow", response_model=Dict[str, Any])
def simulate_slow_response(delay: int = None, db: Session = Depends(get_db)):
    """
    Simulates slow database queries with configurable delay.
    Use ?delay=X to specify delay in seconds (default: random 2-5 seconds)
    """
    if delay is None:
        delay = random.randint(2, 5)
    
    start_time = time.time()
    
    # Simulate slow database operation
    time.sleep(delay)
    
    # Perform actual database query to generate realistic telemetry
    note_count = db.query(Note).count()
    
    end_time = time.time()
    actual_delay = round(end_time - start_time, 2)
    
    return {
        "message": f"Simulated slow operation completed",
        "requested_delay": delay,
        "actual_delay": actual_delay,
        "note_count": note_count,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/error", response_model=Dict[str, Any])
def simulate_error(error_rate: float = 0.5, db: Session = Depends(get_db)):
    """
    Generates random errors based on error_rate (0.0-1.0).
    Default 50% chance of error.
    """
    if random.random() < error_rate:
        error_type = random.choice([
            "database_connection",
            "internal_server_error", 
            "service_unavailable",
            "timeout"
        ])
        
        error_messages = {
            "database_connection": "Database connection failed",
            "internal_server_error": "Internal server error occurred",
            "service_unavailable": "Service temporarily unavailable",
            "timeout": "Request timeout occurred"
        }
        
        status_codes = {
            "database_connection": 503,
            "internal_server_error": 500,
            "service_unavailable": 503,
            "timeout": 504
        }
        
        raise HTTPException(
            status_code=status_codes[error_type],
            detail=error_messages[error_type]
        )
    
    # Success case
    note_count = db.query(Note).count()
    return {
        "message": "Operation successful (no error this time)",
        "error_rate": error_rate,
        "note_count": note_count,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/memory", response_model=Dict[str, Any])
def simulate_memory_intensive(size_mb: int = None):
    """
    Simulates memory-intensive operations.
    Use ?size_mb=X to specify memory allocation in MB (default: random 10-50 MB)
    """
    if size_mb is None:
        size_mb = random.randint(10, 50)
    
    start_time = time.time()
    
    # Simulate memory allocation
    data = []
    try:
        # Allocate memory (1MB = 1024*1024 bytes, using list of strings)
        for _ in range(size_mb * 100):  # Approximate memory usage
            data.append("x" * 10240)  # 10KB strings
        
        # Hold memory for a moment
        time.sleep(1)
        
        # Clean up
        del data
        
    except MemoryError:
        raise HTTPException(status_code=507, detail="Insufficient memory")
    
    end_time = time.time()
    duration = round(end_time - start_time, 2)
    
    return {
        "message": f"Memory operation completed",
        "allocated_mb": size_mb,
        "duration": duration,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/database-load", response_model=Dict[str, Any])
def simulate_database_load(queries: int = None, db: Session = Depends(get_db)):
    """
    Creates heavy database load with multiple queries.
    Use ?queries=X to specify number of queries (default: random 10-50)
    """
    if queries is None:
        queries = random.randint(10, 50)
    
    start_time = time.time()
    results = []
    
    for i in range(queries):
        # Mix of different query types to stress the database
        if i % 3 == 0:
            # Count query
            count = db.query(Note).count()
            results.append(f"count_{i}: {count}")
        elif i % 3 == 1:
            # Order by query
            notes = db.query(Note).order_by(Note.id.desc()).limit(5).all()
            results.append(f"ordered_{i}: {len(notes)} notes")
        else:
            # Filter query
            notes = db.query(Note).filter(Note.locked == False).all()
            results.append(f"filtered_{i}: {len(notes)} unlocked notes")
        
        # Small delay between queries
        time.sleep(0.1)
    
    end_time = time.time()
    duration = round(end_time - start_time, 2)
    
    return {
        "message": f"Database load test completed",
        "queries_executed": queries,
        "duration": duration,
        "sample_results": results[:5],  # First 5 results
        "timestamp": datetime.now().isoformat()
    }

@router.get("/timeout", response_model=Dict[str, Any])
def simulate_timeout(timeout_chance: float = 0.3):
    """
    Simulates connection timeouts.
    Use ?timeout_chance=X (0.0-1.0) to set timeout probability (default: 30%)
    """
    if random.random() < timeout_chance:
        # Simulate a very long operation that would timeout
        time.sleep(10)  # This will likely cause a timeout in most clients
        return {"message": "This shouldn't be reached due to timeout"}
    
    # Normal operation
    time.sleep(random.uniform(0.5, 2.0))  # Some normal delay
    
    return {
        "message": "Operation completed without timeout",
        "timeout_chance": timeout_chance,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/random", response_model=Dict[str, Any])
def simulate_random_behavior(db: Session = Depends(get_db)):
    """
    Randomly selects one of the above simulation behaviors.
    Useful for generating varied telemetry data.
    """
    behaviors = [
        ("slow", lambda: simulate_slow_response(db=db)),
        ("error", lambda: simulate_error(db=db)),
        ("memory", lambda: simulate_memory_intensive()),
        ("database_load", lambda: simulate_database_load(db=db)),
        ("timeout", lambda: simulate_timeout()),
    ]
    
    behavior_name, behavior_func = random.choice(behaviors)
    
    try:
        result = behavior_func()
        result["simulation_type"] = behavior_name
        return result
    except Exception as e:
        # Re-raise HTTP exceptions
        if isinstance(e, HTTPException):
            raise e
        # Handle other exceptions
        raise HTTPException(status_code=500, detail=f"Random simulation error: {str(e)}")

@router.get("/status", response_model=Dict[str, Any])
def simulation_status():
    """
    Returns information about available simulation endpoints.
    """
    return {
        "message": "Simulation service is running",
        "available_endpoints": {
            "/slow": "Simulates slow database operations (2-5 sec delay)",
            "/error": "Generates random errors (50% chance by default)",
            "/memory": "Simulates memory-intensive operations (10-50 MB)",
            "/database-load": "Creates heavy database load (10-50 queries)",
            "/timeout": "Simulates connection timeouts (30% chance)",
            "/random": "Randomly selects one of the above behaviors",
            "/status": "This endpoint - shows simulation service status"
        },
        "usage_tips": {
            "slow": "Use ?delay=5 to set specific delay",
            "error": "Use ?error_rate=0.8 for 80% error rate",
            "memory": "Use ?size_mb=100 for 100MB allocation",
            "database_load": "Use ?queries=25 for 25 database queries",
            "timeout": "Use ?timeout_chance=0.5 for 50% timeout chance"
        },
        "timestamp": datetime.now().isoformat()
    }
