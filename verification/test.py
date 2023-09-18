import requests

# Your YouTube API Key
api_key = "AIzaSyCpbsfCRnsgdzjN5-uEslF66YqWbo7AtsE"

# Search query
search_query = "TomCruisemotivational"

# URL for the YouTube Data API search endpoint
search_url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&part=snippet&type=video&q={search_query}"

# Send GET request to the API endpoint
response = requests.get(search_url)
data = response.json()

# Extract video IDs from the search results
video_ids = [item["id"]["videoId"] for item in data["items"]]

# Construct video URLs using the video IDs
video_urls = [f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids[:5]]

# Print the video URLs
for url in video_urls:
    print(url)