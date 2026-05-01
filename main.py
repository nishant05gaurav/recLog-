import time
import os
from fetcher import fetchMyArticles
from summarizer import generateSummary
from injector import injectArticleCard

def updateArticle():
    """
    This function handles the complete automation flow:
    1. Fetch latest articles
    2. Check for unique articles (via URL and Title)
    3. Inject only new articles into portfolio
    """

    print("Starting Portfolio Update Process")

    # Fetching articles
    articles = fetchMyArticles()

    # If no articles found
    if not articles:
        print("No articles found on Dev.to. Nothing to update.")
        return

    # Reading existing content to prevent duplicates
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            existingContent = f.read()
    except FileNotFoundError:
        existingContent = ""

    # Check Title & URL to prevent from 'Numerous' duplication 
    newArticles = []
    for a in articles:
        if a['url'] not in existingContent and a['title'] not in existingContent:
            newArticles.append(a)

    if not newArticles:
        print("No new unique articles to add. Everything is up to date!")
        return
    
    print(f"Found {len(newArticles)} new articles. Starting injection")

    # Looping through all NEW articles 
    for latest in newArticles:
        print(f"Working on: {latest['title']}")

        # Summary generation 
        print("Generating Summary")
        summaryByAi = generateSummary(latest['body_markdown'])

        # Injecting into HTML
        print(f"Updating portfolio UI for: {latest['title']}")
        isInserted = injectArticleCard(latest, summaryByAi)

        # Final status and refreshing existingContent for next loop
        if isInserted:
            print(f"Done! Portfolio updated with: {latest['title']}")
            # Refresh content so the next article in the loop doesn't re-check old data
            try:
                with open('index.html', 'r', encoding='utf-8') as f:
                    existingContent = f.read()
            except:
                pass
        else:
            print(f"Something went wrong while updating: {latest['title']}")

if __name__ == "__main__":
    updateArticle()