import os
from typing import List

from dotenv import load_dotenv

from models.Article import Article
from models.Suggestion import Suggestion
from services.Browser import Browser
from services.GooglePlaces import GooglePlaces
from services.Twilio import Twilio

load_dotenv()  # take environment variables from .env.

browser = Browser()
google = GooglePlaces()
twilio = Twilio()


def getFirstFourArticles() -> List[Article]:
    parser = browser.navigateTo("https://www.thrillist.com/philadelphia")
    cards = parser.find_all(
        "div",
        class_="UniversalContentCardstyles__UCCTextBlock-sc-r8ldlw-0 hWJlON",
        recursive=True,
    )[:4]

    articles = []
    for card in cards:
        activityType = card.find_all("a", recursive=True)[0].text
        href = (
            "https://www.thrillist.com" + card.find_all("a", recursive=True)[1]["href"]
        )
        h2 = card.find("h2", recursive=True).text
        h3 = card.find("h3", recursive=True).text

        newArticle = Article(activityType, href, h2, h3)
        articles.append(newArticle)
    return articles


def getSuggestions(article) -> List[Suggestion]:
    parser = browser.navigateTo(article.href)

    content = parser.find(
        "div",
        class_="NodeArticlestyles__ObscuredContentWrapper-sc-1dhoc8d-6 hUqleM",
        recursive=True,
    )

    h2s = content.find_all("h2", recursive=True)

    suggestions1 = []

    BASE_URL = "https://www.thrillist.com"

    for h2 in h2s:
        title = h2.text
        a = h2.parent if h2.parent.name == "a" else h2.find("a", recursive=True)
        if not a:
            continue
        href = a["href"]
        href = href if "http" in href else BASE_URL + href

        newSuggestion = Suggestion(title, href)
        suggestions1.append(newSuggestion)
    return suggestions1


def createAndSendMessage(article, suggestions1) -> None:
    origin_id = google.queryPlaceId(os.environ["HOME_ADDRESS"])

    body = ""

    emojisDict = {"eat": "🍔🍔🍔", "lifestyle": "🗿🗿🗿", "events": "🎪🎪🎪"}

    body += f"{emojisDict[article.activity.lower()]} {article.title}\n"

    for idx, suggestion in enumerate(suggestions1):
        body += "\n"
        body += f"{idx + 1}. "

        destination_id = google.queryPlaceId(suggestion.title)

        if destination_id is not None:
            openText = google.queryOpenHours(destination_id)
            etaAndMode = google.queryETAAndMode(origin_id, destination_id)

            body += (
                f"{suggestion.title} ({openText}) - {etaAndMode} - {suggestion.href}"
            )

    twilio.sendSMS(body)


def main():
    articles = getFirstFourArticles()
    for article in articles:
        suggestions1 = getSuggestions(article)
        createAndSendMessage(article, suggestions1)


if __name__ == "__main__":
    main()
