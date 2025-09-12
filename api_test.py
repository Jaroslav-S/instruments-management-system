import requests
from datetime import date

# --- Nastavení ---
BASE_URL = "http://127.0.0.1:8000/instruments/api/"
TOKEN = "d996554aa094bdd30f9aef7d5378962d42c56fc6"  # nahraď tokenem testuser

HEADERS = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

# ------------------------
# --- CRUD Funkce pro Inventory ---
# ------------------------
def create_inventory():
    data = {
        "inv_num": "6001",
        "group": "smyčce",
        "subgroup": "housle",
        "subsubgroup": "nástroj",
        "item": "Housle 4/4",
        "description": "Stradivarius Test",
        "serial_number": "S6001"
    }
    resp = requests.post(BASE_URL + "inventory/", json=data, headers=HEADERS)
    print("Inventory created:", resp.status_code, resp.json())
    return resp.json()

def update_inventory(inv_id):
    data = {"description": "Stradivarius Test v2"}
    resp = requests.patch(BASE_URL + f"inventory/{inv_id}/", json=data, headers=HEADERS)
    print("Inventory updated:", resp.status_code, resp.json())

def delete_inventory(inv_id):
    resp = requests.delete(BASE_URL + f"inventory/{inv_id}/", headers=HEADERS)
    print("Inventory deleted:", resp.status_code)

# ------------------------
# --- CRUD Funkce pro Purchases ---
# ------------------------
def create_purchase(inv_id):
    data = {
        "inventory_item": inv_id,
        "purchase_date": str(date.today()),
        "supplier": "Hudební dům",
        "amount": 25000,
        "currency": "CZK",
        "invoice": "F6001",
        "notes": "První nákup"
    }
    resp = requests.post(BASE_URL + "purchases/", json=data, headers=HEADERS)
    print("Purchase created:", resp.status_code, resp.json())
    return resp.json()

def update_purchase(p_id):
    data = {"notes": "Poznámka aktualizována"}
    resp = requests.patch(BASE_URL + f"purchases/{p_id}/", json=data, headers=HEADERS)
    print("Purchase updated:", resp.status_code, resp.json())

def delete_purchase(p_id):
    resp = requests.delete(BASE_URL + f"purchases/{p_id}/", headers=HEADERS)
    print("Purchase deleted:", resp.status_code)

# ------------------------
# --- CRUD Funkce pro Servicing ---
# ------------------------
def create_service(inv_id):
    data = {
        "inventory_item": inv_id,
        "service_date": str(date.today()),
        "supplier": "Servis s.r.o.",
        "amount": 2000,
        "currency": "CZK",
        "invoice": "S6001",
        "notes": "Ladění strun"
    }
    resp = requests.post(BASE_URL + "servicing/", json=data, headers=HEADERS)
    print("Service created:", resp.status_code, resp.json())
    return resp.json()

def update_service(s_id):
    data = {"notes": "Servis ladění"}
    resp = requests.patch(BASE_URL + f"servicing/{s_id}/", json=data, headers=HEADERS)
    print("Service updated:", resp.status_code, resp.json())

def delete_service(s_id):
    resp = requests.delete(BASE_URL + f"servicing/{s_id}/", headers=HEADERS)
    print("Service deleted:", resp.status_code)

# ------------------------
# --- CRUD Funkce pro Rentals ---
# ------------------------
def create_rental(inv_id):
    data = {
        "inventory_item": inv_id,
        "action_date": str(date.today()),
        "rental_type": "loan",
        "renter_name": "Filharmonie Praha",
        "notes": "Na koncert"
    }
    resp = requests.post(BASE_URL + "rentals/", json=data, headers=HEADERS)
    print("Rental created:", resp.status_code, resp.json())
    return resp.json()

def update_rental(r_id):
    data = {"notes": "Na koncert + zkouška"}
    resp = requests.patch(BASE_URL + f"rentals/{r_id}/", json=data, headers=HEADERS)
    print("Rental updated:", resp.status_code, resp.json())

def delete_rental(r_id):
    resp = requests.delete(BASE_URL + f"rentals/{r_id}/", headers=HEADERS)
    print("Rental deleted:", resp.status_code)

# ------------------------
# --- CRUD Funkce pro Disposals ---
# ------------------------
def create_disposal(inv_id):
    data = {
        "inventory_item": inv_id,
        "disposal_date": str(date(2030, 1, 1)),
        "disposal_reason": "vyřazení",
        "notes": "Archivováno v DB"
    }
    resp = requests.post(BASE_URL + "disposals/", json=data, headers=HEADERS)
    print("Disposal created:", resp.status_code, resp.json())
    return resp.json()

def update_disposal(d_id):
    data = {"notes": "Archivováno"}
    resp = requests.patch(BASE_URL + f"disposals/{d_id}/", json=data, headers=HEADERS)
    print("Disposal updated:", resp.status_code, resp.json())

def delete_disposal(d_id):
    resp = requests.delete(BASE_URL + f"disposals/{d_id}/", headers=HEADERS)
    print("Disposal deleted:", resp.status_code)

# ------------------------
# --- Main ---
# ------------------------
def main():
    # --- Inventory ---
    inv = create_inventory()
    inv_id = inv["id"]
    update_inventory(inv_id)

    # --- Purchases ---
    purchase = create_purchase(inv_id)
    p_id = purchase["id"]
    update_purchase(p_id)

    # --- Servicing ---
    service = create_service(inv_id)
    s_id = service["id"]
    update_service(s_id)

    # --- Rentals ---
    rental = create_rental(inv_id)
    r_id = rental["id"]
    update_rental(r_id)

    # --- Disposals ---
    disposal = create_disposal(inv_id)
    d_id = disposal["id"]
    update_disposal(d_id)

    # --- Cleanup ---
    delete_disposal(d_id)
    delete_rental(r_id)
    delete_service(s_id)
    delete_purchase(p_id)
    delete_inventory(inv_id)

if __name__ == "__main__":
    main()