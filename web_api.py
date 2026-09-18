"""
Web API for the Airline Reservation System.

Wraps the existing DSA-powered services (Hash Table auth, AVL Tree
flight/booking storage, Graph + Dijkstra route finder, Min-Heap waiting
list) behind a REST API, and serves the web frontend from /web.
"""

import os
import secrets
import threading
from datetime import date, timedelta
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from database.database import setup_database, insert_sample_data
from services import data_store
from services.auth_service import AuthService
from services.flight_service import FlightService
from services.reservation_service import ReservationService
from services.cancellation_service import CancellationService
from algorithms.dijkstra import find_shortest_path

# ----------------------------------------------------------------------------
# App setup
# ----------------------------------------------------------------------------

_lock = threading.RLock()
_tokens = {}  # token -> user dict (in-memory sessions)

app = FastAPI(title="Airline Reservation System API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------------------------------------------------
# Startup: initialize DB, load data into the DSA structures, seed flights
# ----------------------------------------------------------------------------

def seed_upcoming_flights():
    """If no flights are scheduled for today or later, generate a week of them."""
    today = date.today()
    existing = FlightService.get_all_flights()
    if any(f.flight_date >= today.isoformat() for f in existing):
        return

    routes = [
        ("DEL", "BOM", 1150), ("DEL", "BLR", 1740), ("DEL", "HYD", 1250),
        ("DEL", "CCU", 1300), ("DEL", "JAI", 240), ("BOM", "GOI", 400),
        ("BOM", "BLR", 840), ("BLR", "MAA", 290), ("HYD", "MAA", 520),
        ("BLR", "TRV", 500),
    ]
    airlines = ["Air India", "IndiGo", "SpiceJet", "Vistara", "Akasa Air"]
    times = [("06:00", "08:15"), ("09:30", "11:45"), ("14:00", "16:20"),
             ("18:45", "21:05"), ("21:30", "23:40")]
    seat_plan = [100, 120, 150, 180]

    created = 0
    for offset in range(7):
        d = (today + timedelta(days=offset)).isoformat()
        for i, (src, dst, dist) in enumerate(routes):
            airline = airlines[(i + offset) % len(airlines)]
            dep, arr = times[(i + offset) % len(times)]
            price = float(1500 + int(dist * 2.5 / 50) * 50)
            seats = seat_plan[(i + offset) % len(seat_plan)]
            flight_number = f"AI{200 + offset * 10 + i}"
            ok, _ = FlightService.add_flight(
                flight_number, airline, src, dst, d, dep, arr, seats, price
            )
            created += 1 if ok else 0
    print(f"Seeded {created} upcoming flights for the live site.")


@app.on_event("startup")
def initialize_system():
    setup_database()
    insert_sample_data()
    data_store.load_all_data()
    seed_upcoming_flights()


# ----------------------------------------------------------------------------
# Serialization helpers
# ----------------------------------------------------------------------------

def flight_to_dict(f):
    if f is None:
        return None
    return {
        "flight_number": f.flight_number,
        "airline": f.airline,
        "source": f.source,
        "destination": f.destination,
        "flight_date": f.flight_date,
        "dep_time": f.dep_time,
        "arr_time": f.arr_time,
        "total_seats": f.total_seats,
        "available_seats": f.available_seats,
        "price": f.price,
    }


def booking_to_dict(b, include_flight=True):
    d = {
        "booking_id": b.booking_id,
        "user_id": b.user_id,
        "flight_number": b.flight_number,
        "status": b.status,
        "booking_date": b.booking_date,
    }
    if include_flight:
        fl = FlightService.search_flight(b.flight_number)
        d["flight"] = flight_to_dict(fl)
    d["passenger"] = ReservationService.get_passenger_details(b.booking_id)
    return d


def user_public(u):
    return {"user_id": u["user_id"], "username": u["username"],
            "name": u["name"], "role": u["role"]}


# ----------------------------------------------------------------------------
# Auth dependencies
# ----------------------------------------------------------------------------

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = _tokens.get(authorization[7:])
    if not user:
        raise HTTPException(status_code=401, detail="Session expired. Please log in again.")
    return user


def require_admin(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


# ----------------------------------------------------------------------------
# Schemas
# ----------------------------------------------------------------------------

class LoginInput(BaseModel):
    username: str
    password: str


class RegisterInput(BaseModel):
    name: str
    username: str
    password: str


class PassengerInfo(BaseModel):
    full_name: str
    age: Optional[int] = None
    gender: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""


class BookingInput(BaseModel):
    flight_number: str
    passenger: Optional[PassengerInfo] = None


class FlightInput(BaseModel):
    flight_number: str
    airline: str
    source: str
    destination: str
    flight_date: str
    dep_time: str
    arr_time: str
    total_seats: int
    price: float


# ----------------------------------------------------------------------------
# Auth endpoints
# ----------------------------------------------------------------------------

@app.post("/api/login")
def login(body: LoginInput):
    with _lock:
        user = AuthService.login(body.username.strip(), body.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = secrets.token_hex(24)
    _tokens[token] = user
    return {"token": token, "user": user_public(user)}


@app.post("/api/register")
def register(body: RegisterInput):
    with _lock:
        ok, message = AuthService.register_passenger(
            body.name.strip(), body.username.strip(), body.password
        )
    if not ok:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message}


@app.get("/api/me")
def me(user=Depends(get_current_user)):
    return {"user": user_public(user)}


@app.post("/api/logout")
def logout(user=Depends(get_current_user)):
    for t, u in list(_tokens.items()):
        if u is user:
            _tokens.pop(t, None)
    return {"message": "Logged out"}


# ----------------------------------------------------------------------------
# Public data endpoints
# ----------------------------------------------------------------------------

@app.get("/api/airports")
def airports():
    return {"airports": sorted(data_store.airport_graph.nodes.keys())}


@app.get("/api/flights")
def list_flights(source: Optional[str] = None, destination: Optional[str] = None):
    with _lock:
        flights = [flight_to_dict(f) for f in FlightService.get_all_flights()]
    if source:
        flights = [f for f in flights if f["source"] == source]
    if destination:
        flights = [f for f in flights if f["destination"] == destination]
    return {"flights": flights}


@app.get("/api/flights/{flight_number}")
def get_flight(flight_number: str):
    with _lock:
        f = FlightService.search_flight(flight_number)
    if not f:
        raise HTTPException(status_code=404, detail="Flight not found")
    return {"flight": flight_to_dict(f)}


@app.get("/api/route")
def shortest_route(
    origin: str = Query(..., alias="from"),
    destination: str = Query(..., alias="to"),
):
    with _lock:
        path, dist = find_shortest_path(data_store.airport_graph, origin.upper(), destination.upper())
    if not path:
        raise HTTPException(status_code=404, detail=f"No route found between {origin} and {destination}")
    return {"path": path, "total_distance_km": dist, "stops": max(len(path) - 2, 0)}


# ----------------------------------------------------------------------------
# Passenger endpoints
# ----------------------------------------------------------------------------

@app.post("/api/bookings")
def create_booking(body: BookingInput, user=Depends(get_current_user)):
    with _lock:
        info = body.passenger.model_dump() if body.passenger else None
        ok, message = ReservationService.book_ticket(user["user_id"], body.flight_number.strip().upper(), info)
    if not ok and "Flight not found" in message:
        raise HTTPException(status_code=404, detail=message)
    return {"success": ok, "message": message}


@app.get("/api/bookings")
def my_bookings(user=Depends(get_current_user)):
    with _lock:
        bookings = [booking_to_dict(b) for b in CancellationService.get_user_bookings(user["user_id"])]
    return {"bookings": bookings}


@app.delete("/api/bookings/{booking_id}")
def cancel_booking(booking_id: str, user=Depends(get_current_user)):
    with _lock:
        node = data_store.booking_tree.search(data_store.booking_root, booking_id)
        if not node:
            raise HTTPException(status_code=404, detail="Booking not found")
        if node.data.user_id != user["user_id"] and user["role"] != "admin":
            raise HTTPException(status_code=403, detail="You can only cancel your own bookings")
        ok, message = CancellationService.cancel_booking(booking_id)
    return {"success": ok, "message": message}


# ----------------------------------------------------------------------------
# Admin endpoints
# ----------------------------------------------------------------------------

@app.post("/api/admin/flights")
def admin_add_flight(body: FlightInput, user=Depends(require_admin)):
    with _lock:
        ok, message = FlightService.add_flight(
            body.flight_number.strip().upper(), body.airline.strip(),
            body.source.strip().upper(), body.destination.strip().upper(),
            body.flight_date, body.dep_time, body.arr_time,
            body.total_seats, body.price,
        )
    if not ok:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message}


@app.delete("/api/admin/flights/{flight_number}")
def admin_delete_flight(flight_number: str, user=Depends(require_admin)):
    with _lock:
        ok, message = FlightService.delete_flight(flight_number.strip().upper())
    return {"message": message}


@app.get("/api/admin/bookings")
def admin_all_bookings(user=Depends(require_admin)):
    with _lock:
        nodes = data_store.booking_tree.inorder_traversal(data_store.booking_root)
        bookings = [booking_to_dict(n[1]) for n in nodes]
    return {"bookings": bookings}


@app.get("/api/admin/waitlist")
def admin_waitlist(user=Depends(require_admin)):
    with _lock:
        entries = sorted(
            [{"wait_id": n.data["wait_id"], "user_id": n.data["user_id"],
              "flight_number": n.data["flight_number"], "priority": n.priority}
             for n in data_store.waiting_list_pq.heap],
            key=lambda e: e["priority"],
        )
    return {"waitlist": entries}


@app.get("/api/admin/stats")
def admin_stats(user=Depends(require_admin)):
    with _lock:
        flights = FlightService.get_all_flights()
        nodes = data_store.booking_tree.inorder_traversal(data_store.booking_root)
        confirmed = [n[1] for n in nodes if n[1].status == "CONFIRMED"]
        revenue = 0.0
        for b in confirmed:
            fl = FlightService.search_flight(b.flight_number)
            if fl:
                revenue += fl.price
        return {
            "total_flights": len(flights),
            "confirmed_bookings": len(confirmed),
            "cancelled_bookings": sum(1 for n in nodes if n[1].status == "CANCELLED"),
            "waitlist_count": len(data_store.waiting_list_pq.heap),
            "revenue": revenue,
        }


# ----------------------------------------------------------------------------
# Static frontend (must be mounted last so /api routes win)
# ----------------------------------------------------------------------------

web_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
app.mount("/", StaticFiles(directory=web_dir, html=True), name="web")
