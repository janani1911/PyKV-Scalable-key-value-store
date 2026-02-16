import streamlit as st
import requests
import pandas as pd
from pykv.features.store.kv_store import PyKVStore


BASE_URL = "http://127.0.0.1:8000"

st.title("🗄️ PyKV Store – LRU Demo")

key = st.text_input("Key")
value = st.text_input("Value")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("SET"):
        st.success(requests.post(
            f"{BASE_URL}/set",
            json={"key": key, "value": value}
        ).json())

with col2:
    if st.button("GET"):
        r = requests.get(f"{BASE_URL}/get/{key}")
        if r.status_code == 200:
            st.info(r.json())
        else:
            st.error("Key not found")

with col3:
    if st.button("DELETE"):
        st.warning(requests.delete(
            f"{BASE_URL}/delete/{key}"
        ).json())

st.divider()

if st.button("SHOW ALL CACHE (LRU CHECK)"):
    r = requests.get(f"{BASE_URL}/all").json()

    st.subheader("📦 Current Cache Data")
    df = pd.DataFrame(r["data"].items(), columns=["Key", "Value"])
    st.table(df)

    st.subheader("⏳ LRU Order (Least → Most Recent)")
    st.write(r["lru_order"])

    st.info(f"Capacity: {r['capacity']} | Current Size: {r['current_size']}")
