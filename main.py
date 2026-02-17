import os
import requests
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="Free Fire ID Checker")

@app.get("/")
def home():
    return {"message": "FF ID Checker API is running. Use /check/{uid}?region={region}"}

@app.get("/check/{uid}")
def check_free_fire_id(
    uid: str, 
    region: str = Query("sg", description="Regions: sg, ind, br, me, etc.")
):
    # Current active community endpoint for 2026 (OB51+)
    # If this specific link expires, you can replace it with any active lookup URL
    url = f"https://info-ob49.vercel.app/api/account/?uid={uid}&region={region}"

    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="UID not found or API is down.")

        data = response.json()
        
        # Mapping common API response fields to a clean format
        # Third-party APIs often change their JSON keys, so we check a few possibilities
        info = data.get("basicinfo") or data
        nickname = info.get("nickname") or info.get("PlayerName") or "Unknown"
        
        return {
            "status": "success",
            "uid": uid,
            "nickname": nickname,
            "level": info.get("level", "N/A"),
            "region": region.upper(),
            "full_data": data  # Returns the full original data if you need more details
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Use the port Render assigns, defaulting to 8000 for local testing
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
