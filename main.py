import os
from urllib.parse import urljoin, urlparse
import requests
import io
from bs4 import BeautifulSoup


def main():
    club_urls = [
        "https://www.transfermarkt.com/fc-bayern-munchen/startseite/verein/27/saison_id/2023",
        "https://www.transfermarkt.com/bayer-04-leverkusen/startseite/verein/15/saison_id/2023",
        "https://www.transfermarkt.com/rasenballsport-leipzig/startseite/verein/23826/saison_id/2023",
        "https://www.transfermarkt.com/borussia-dortmund/startseite/verein/16/saison_id/2023",
        "https://www.transfermarkt.com/vfl-wolfsburg/startseite/verein/82/saison_id/2023",
        "https://www.transfermarkt.com/vfb-stuttgart/startseite/verein/79/saison_id/2023",
        "https://www.transfermarkt.com/eintracht-frankfurt/startseite/verein/24/saison_id/2023",
        "https://www.transfermarkt.com/borussia-monchengladbach/startseite/verein/18/saison_id/2023",
        "https://www.transfermarkt.com/sc-freiburg/startseite/verein/60/saison_id/2023",
        "https://www.transfermarkt.com/1-fc-union-berlin/startseite/verein/89/saison_id/2023",
        "https://www.transfermarkt.com/tsg-1899-hoffenheim/startseite/verein/533/saison_id/2023",
        "https://www.transfermarkt.com/fc-augsburg/startseite/verein/167/saison_id/2023",
        "https://www.transfermarkt.com/1-fsv-mainz-05/startseite/verein/39/saison_id/2023",
        "https://www.transfermarkt.com/sv-werder-bremen/startseite/verein/86/saison_id/2023",
        "https://www.transfermarkt.com/1-fc-koln/startseite/verein/3/saison_id/2023",
        "https://www.transfermarkt.com/vfl-bochum/startseite/verein/80/saison_id/2023",
        "https://www.transfermarkt.com/1-fc-heidenheim-1846/startseite/verein/2036/saison_id/2023",
        "https://www.transfermarkt.com/sv-darmstadt-98/startseite/verein/105/saison_id/2023"

    ]
    images(club_urls)


def images(club_urls):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'}

    for club_url in club_urls:
        response = requests.get(club_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.select('img[data-src^="https://img.a.transfermarkt.technology/portrait/medium/"]')

            save_directory = 'player_images'
            club_name = club_url.split('/')[-6]  # Extract club name from URL
            club_directory = os.path.join(save_directory, club_name)
            os.makedirs(club_directory, exist_ok=True)

            for img_tag in img_tags:
                data_src_attribute = img_tag.get('data-src')
                if data_src_attribute:
                    img_url = data_src_attribute

                    player_name_tag = img_tag.find_next('a')
                    if player_name_tag:
                        player_name = player_name_tag.get_text(strip=True)
                        name_parts = player_name.split()
                        reversed_name = '_'.join(name_parts[::-1]).lower()
                        img_name = f"{reversed_name}.webp"
                        img_path = os.path.join(club_directory, img_name)

                        img_data = requests.get(img_url).content
                        with open(img_path, 'wb') as f:
                            f.write(img_data)

                        print(f"Image {img_name} saved successfully for {club_name}.")
                    else:
                        print("Skipping image without adjacent <a> tag.")
                else:
                    print("Skipping image without 'data-src' attribute.")

        else:
            print(f"Failed to retrieve the page {club_url}. Status code: {response.status_code}")  # handle error


if __name__ == "__main__":
    main()
