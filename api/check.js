// api/check.js
export default async function handler(req, res) {
  const { id, zone } = req.query;

  // 1. Basic Validation
  if (!id || !zone) {
    return res.status(400).json({ 
      success: false, 
      message: "Please provide both 'id' and 'zone' parameters." 
    });
  }

  try {
    // 2. Fetch data from the community scraper API
    const response = await fetch(`https://api.isan.eu.org/nickname/ml?id=${id}&zone=${zone}`);
    const data = await response.json();

    // 3. Check if nickname was found
    if (data.success && data.name) {
      return res.status(200).json({
        success: true,
        nickname: data.name,
        id: id,
        zone: zone
      });
    } else {
      return res.status(404).json({
        success: false,
        message: "Player not found. Check your ID and Zone ID."
      });
    }
  } catch (error) {
    return res.status(500).json({ 
      success: false, 
      message: "Internal Server Error", 
      error: error.message 
    });
  }
}
