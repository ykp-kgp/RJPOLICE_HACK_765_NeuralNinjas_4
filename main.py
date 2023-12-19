#storing into csv file

import requests
from bs4 import BeautifulSoup
import csv

# URL of the main page containing chapter links
main_url = "https://devgan.in/ipc/"

# Fetch the main page
response = requests.get(main_url)
soup = BeautifulSoup(response.content, "html.parser")

# Find all chapter links
chapter_links = soup.select("table.menu td:nth-child(2) a")

# Create a CSV file
with open("ipc_sections.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Chapter Number", "Chapter", "Section Number", "Section Title", "Section Content"])

    # Loop through each chapter link
    for chapter_link in chapter_links:
        chapter_url = f"https://devgan.in{chapter_link['href']}"
        chapter_name = chapter_link.text.strip()

        # Fetch the content of the chapter
        chapter_response = requests.get(chapter_url)
        chapter_soup = BeautifulSoup(chapter_response.content, "html.parser")

        # Find all sections under the current chapter
        sections = chapter_soup.find_all("h2")

        # Write Chapter Number and Chapter Name
        writer.writerow(["", chapter_name, "", "", ""])

        # Extract details for each section
        for section in sections:
            if section.find("a"):  # Check if the section contains an anchor tag for the section number
                section_number = section.find("a").text.strip()
                section_title = section.text.split(":-")[1].strip() if ":-" in section.text else section.text.strip()
                section_content = section.find_next("div", class_="sectxt").text.strip()

                # Write to CSV
                writer.writerow(["", "", section_number, section_title, section_content])

print("Data has been saved to ipc_sections.csv")