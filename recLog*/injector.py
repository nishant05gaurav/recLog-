import os
from bs4 import BeautifulSoup, Comment

# Path to the HTML file where article cards will be injected
HTML_FILE_PATH = "index.html"

# Anchor text used to identify the exact insertion point in the HTML
ANCHOR_TEXT = "AUTOMATION: INSERT ARTICLES HERE"

def isMyAnchhorComment(text):
    """
    Check whether a given text node is the target anchor comment.This function is used while parsing HTML to identify the specific    comment node that marks where new article cards should be inserted.

    Args:
        text: A BeautifulSoup text node.

    Returns:
        bool: True if the node is a comment and contains the anchor text,
              otherwise False.
    """
    
    # Checking if the node is a comment
    isItComment = isinstance(text, Comment)
    
    # Checking if the comment contains the anchor text
    hasAnchor = ANCHOR_TEXT in text
    
    # Returning True only if both conditions are satisfied
    return isItComment and hasAnchor


def injectArticleCard(articleData, summaryByAi):
    """
    Inject a new article card into the HTML file at the anchor location. This function reads the existing HTML file, finds the anchor comment, and inserts a new article card right after it. The card includes article title, image, summary, and link.

    Args:
        articleData (dict): Dictionary containing article details like title, url, and coverImage.
        summaryByAi (str): AI-generated summary of the article.

    Returns:
        bool: True if the card was successfully inserted, otherwise False.
    """
    
    # Logging which article is being processed
    print(f"Processing article: {articleData['title']}")

    # Handling case - HTML file does not exist
    if not os.path.exists(HTML_FILE_PATH):
        print(f"File not found: {HTML_FILE_PATH}")
        return False

    # Reading and parsing the HTML file
    with open(HTML_FILE_PATH, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    
    # Searching for the anchor comment in the HTML
    lookForComment = soup.find(string=isMyAnchhorComment)
    
    # Handling case - anchor comment not found
    if not lookForComment:
        print("Anchor comment not found in HTML. Skipping injection.")
        return False

    # Retrieving the primary image URL from article data
    imageUrlPrimary = articleData.get('coverImage')
    
    # Handling case - no image available
    if not imageUrlPrimary:
        imageUrlPrimary = 'https://via.placeholder.com/600x300?text=No+Image'

    # Creating the HTML structure for the new article card
    newCardHTML = f"""
    <div class="col-12 mb-3 auto-generated-card">
        <div class="card shadow-sm border-0 h-100 overflow-hidden" style="max-width: 800px; margin: 0 auto;">
            <div class="row g-0 align-items-stretch h-100">
                <div class="col-md-4">
                    <img src="{imageUrlPrimary}" 
                         class="img-fluid rounded-start w-100" 
                         alt="{articleData['title']} Cover Image"
                         style="object-fit: cover; height: 100%; min-height: 180px;"
                         onerror="this.onerror=null;this.src='https://via.placeholder.com/800x400?text=Image+Not+Available';">
                </div>
                <div class="col-md-8">
                    <div class="card-body p-4 d-flex flex-column justify-content-center h-100">
                        <span class="text-uppercase fw-bold mb-1 d-block" style="color: var(--warm-orange); font-size: 0.8rem;">
                            Latest Insight
                        </span>
                        <h5 class="card-title text-dark fw-bold mb-3">{articleData['title']}</h5>
                        <p class="card-text text-muted small mb-3" style="font-size: 0.85rem;">{summaryByAi}</p>
                        <div>
                            <a href="{articleData['url']}" target="_blank" class="article-btn" style="font-size: 0.8rem; padding: 6px 15px;">
                                Read on Dev.to <i class="fas fa-arrow-right ms-1"></i>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

    # Parsing the new card HTML into BeautifulSoup format
    newCardSoup = BeautifulSoup(newCardHTML, "html.parser")
    
    # Inserting the new card right after the anchor comment
    lookForComment.insert_after(newCardSoup)

    # Writing the updated HTML back to the file
    with open(HTML_FILE_PATH, "w", encoding="utf-8") as file:
        file.write(str(soup))
        
    # Confirming successful insertion
    print("Card inserted successfully in the website")
    
    return True