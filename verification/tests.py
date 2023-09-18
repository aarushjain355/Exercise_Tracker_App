from django.test import TestCase

# Create your tests here.

person_name = "tomcruise"
search_query = f'{person_name} motivational'
search_url = f'https://www.youtube.com/results?search_query={search_query}'
    
response = requests.get(search_url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    video_links = []

    for link in soup.find_all("a"):
        href = link.get("href")

        if "/watch?v=" in href:
            video_links.append(f'https://www.youtube.com{href}')

            if len(video_links) >= 5:
                break

print(video_links)