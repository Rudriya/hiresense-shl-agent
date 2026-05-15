# scraper/scrape_catalog.py

import json
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


BASE_URL = "https://www.shl.com"

CATALOG_URL = (
    "https://www.shl.com/solutions/products/product-catalog/"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def clean_text(text):

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def get_page(url):

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    return BeautifulSoup(
        response.text,
        "html.parser"
    )


def get_catalog_links():

    soup = get_page(CATALOG_URL)

    links = set()

    for a in soup.find_all("a", href=True):

        href = a["href"]

        # ONLY real assessment pages
        if "/view/" not in href:
            continue

        full_url = urljoin(BASE_URL, href)

        full_url = (
            full_url
            .split("?")[0]
            .split("#")[0]
        )

        links.add(full_url)

    return sorted(list(links))


def extract_test_type(text):

    text = text.lower()

    detected = []

    personality_keywords = [
        "personality",
        "behavioral",
        "motivation",
        "opq"
    ]

    cognitive_keywords = [
        "cognitive",
        "aptitude",
        "reasoning",
        "numerical",
        "verbal"
    ]

    technical_keywords = [
        "coding",
        "technical",
        "developer",
        "java",
        "python",
        "software"
    ]

    simulation_keywords = [
        "simulation",
        "situational judgement",
        "scenario"
    ]

    if any(k in text for k in personality_keywords):
        detected.append("P")

    if any(k in text for k in cognitive_keywords):
        detected.append("C")

    if any(k in text for k in technical_keywords):
        detected.append("T")

    if any(k in text for k in simulation_keywords):
        detected.append("S")

    return detected


def extract_duration(text):

    patterns = [
        r"(\d+)\s*minutes",
        r"(\d+)\s*mins"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return f"{match.group(1)} minutes"

    return "Not specified"


def extract_skills(text):

    skill_keywords = [
        "java",
        "python",
        "sql",
        "leadership",
        "communication",
        "coding",
        "problem solving",
        "analytical",
        "developer",
        "teamwork",
        "stakeholder"
    ]

    found = []

    lower_text = text.lower()

    for skill in skill_keywords:

        if skill in lower_text:
            found.append(skill)

    return list(set(found))


def scrape_assessment(url):

    try:

        soup = get_page(url)

        title = soup.find("h1")

        title = (
            clean_text(title.text)
            if title
            else ""
        )

        page_text = clean_text(
            soup.get_text(" ", strip=True)
        )

        meta = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        description = (
            meta.get("content")
            if meta
            else page_text[:2000]
        )

        assessment = {
            "name": title,
            "url": url,
            "description": description,
            "duration": extract_duration(page_text),
            "skills": extract_skills(page_text),
            "test_type": extract_test_type(page_text)
        }

        return assessment

    except Exception as e:

        print(f"Error scraping {url}")

        print(e)

        return None


def main():

    print("Fetching catalog links...")

    links = get_catalog_links()

    print(f"Found {len(links)} assessments")

    assessments = []

    for link in tqdm(links):

        item = scrape_assessment(link)

        if item:
            assessments.append(item)

        time.sleep(1)

    with open(
        "app/data/catalog.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            assessments,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("Catalog saved successfully!")


if __name__ == "__main__":

    main()