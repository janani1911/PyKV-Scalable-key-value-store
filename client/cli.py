import requests

BASE_URL = "http://127.0.0.1:8000"

def show_menu():
    print("\n=== PyKV CLI ===")
    print("1. SET key-value")
    print("2. GET value by key")
    print("3. DELETE key")
    print("4. SHOW ALL (LRU CHECK)")
    print("5. EXIT")


while True:
    show_menu()
    choice = input("Choose an option: ").strip()

    # ---------------- SET ----------------
    if choice == "1":
        key = input("Enter key: ").strip()
        value = input("Enter value: ").strip()

        res = requests.post(
            f"{BASE_URL}/set",
            json={"key": key, "value": value}
        )

        if res.status_code == 200:
            print("✅ Key stored successfully")
        else:
            print("❌ Error:", res.text)

    # ---------------- GET ----------------
    elif choice == "2":
        key = input("Enter key: ").strip()

        res = requests.get(f"{BASE_URL}/get/{key}")

        if res.status_code == 200:
            data = res.json()
            print(f"✅ Value: {data['value']}")
        else:
            print("❌ Key not found")

    # ---------------- DELETE ----------------
    elif choice == "3":
        key = input("Enter key to delete: ").strip()

        res = requests.delete(f"{BASE_URL}/delete/{key}")

        if res.status_code == 200:
            print("✅ Key deleted")
        else:
            print("❌ Key not found")

    # ---------------- SHOW ALL (LRU) ----------------
    elif choice == "4":
        res = requests.get(f"{BASE_URL}/all")

        if res.status_code != 200:
            print("❌ Backend error:", res.text)
            continue

        try:
            data = res.json()
        except Exception:
            print("❌ Invalid response from backend")
            print(res.text)
            continue

        print("\n--- CACHE DATA ---")
        if not data["data"]:
            print("(empty)")
        else:
            for k, v in data["data"].items():
                print(f"{k} : {v}")

        print("\n--- LRU ORDER (Least → Most Recent) ---")
        print(data["lru_order"])

        print(f"\nCapacity     : {data['capacity']}")
        print(f"Current Size : {data['current_size']}")

    # ---------------- EXIT ----------------
    elif choice == "5":
        print("👋 Exiting PyKV CLI")
        break

    else:
        print("❌ Invalid option. Try again.")
