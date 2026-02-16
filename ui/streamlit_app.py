import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="PyKV Store", layout="centered")

st.title("🗄️ PyKV In-Memory Key-Value Store")
st.caption("LRU Cache with Persistence")

# ---------------- SET ----------------
st.subheader("➕ Set Key-Value")
key = st.text_input("Key")
value = st.text_input("Value")

if st.button("SET"):
    if key and value:
        res = requests.post(
            f"{BASE_URL}/set",
            json={"key": key, "value": value}
        )
        if res.status_code == 200:
            st.success("Key stored successfully")
        else:
            st.error(res.text)
    else:
        st.warning("Please enter both key and value")

# ---------------- GET ----------------
st.divider()
st.subheader("🔍 Get Value by Key")
get_key = st.text_input("Key to fetch", key="get")

if st.button("GET"):
    if get_key:
        res = requests.get(f"{BASE_URL}/get/{get_key}")
        if res.status_code == 200:
            st.success(f"Value: {res.json()['value']}")
        else:
            st.error("Key not found")

# ---------------- SHOW ALL ----------------
st.divider()
st.subheader("📊 Cache State (LRU Check)")

if st.button("SHOW ALL"):
    res = requests.get(f"{BASE_URL}/all")

    if res.status_code != 200:
        st.error(res.text)
    else:
        data = res.json()

        st.write("### Stored Key-Value Pairs")
        if not data["data"]:
            st.info("Cache is empty")
        else:
            st.json(data["data"])

        st.write("### LRU Order (Least → Most Recent)")
        st.write(data["lru_order"])

        st.write(f"**Capacity:** {data['capacity']}")
        st.write(f"**Current Size:** {data['current_size']}")
