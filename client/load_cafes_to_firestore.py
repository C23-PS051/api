from initialise_firebase_admin import app

from firebase_admin import firestore
import pandas as pd

db = firestore.client()

df = pd.read_csv('./cafe_one_hot.csv')
df = df.reset_index()
i = 0
for index, cafe in df.iterrows():
    i += 1
    current_cafe = {
        "cafe_id": cafe["cafe_id"],
        "address": cafe["alamat"],
        "alcohol": cafe["is_alcohol"] == 1,
        "closing_hour": 24 if cafe["is_24hrs"] == 1 else 22, # placeholder
        "description": "lorem ipsum", # placeholder
        "in_mall": cafe["is_in_mall"] == 1,
        "indoor": cafe["is_indoor"] == 1,
        "kid_friendly": cafe["is_kid_friendly"] == 1,
        "live_music": cafe["is_live_music"] == 1,
        "name": cafe["nama"],
        "opening_hour": 0 if cafe["is_24hrs"] == 1 else 10, # placeholder
        "outdoor": cafe["is_outdoor"] == 1,
        "parking_area": cafe["is_parking_area"] == 1,
        "pet_friendly": cafe["is_pet_friendly"] == 1,
        "price_category": cafe["kategori_harga"],
        "rating": cafe["rating"],
        "region": cafe["region"],
        "reservation": cafe["is_reservation"] == 1,
        "review": cafe["review"],
        "smoking_area": cafe["is_smoking_area"] == 1,
        "takeaway": cafe["is_takeaway"] == 1,
        "toilets": cafe["is_toilets"] == 1,
        "thumbnail_url": "https://images.unsplash.com/photo-1685491107139-7d7f4f17b3eb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=776&q=80",
        "vip_room": cafe["is_vip_room"] == 1,
        "wifi": cafe["is_wifi"],
    }

    cafe_ref = db.collection('cafes').document(cafe["cafe_id"])
    cafe_ref.set(current_cafe)
