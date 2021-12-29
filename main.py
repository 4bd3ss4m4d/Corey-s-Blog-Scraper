# Scraping Corey's Blog

#########################
# Created by 4bd3ss4m4d #
#########################

from bs4 import BeautifulSoup
import requests
import re
import csv


# Number of pages in Corey's blog
COREY_BLOG_PAGES_NUM = 17


# Corey MS's blog scraper
def corey_blog_scraper(URL):
    # Send an HTTP request
    response = requests.get(URL)
    # Raise an exception if something goes wrong
    response.raise_for_status()
    # Create variable that holds html code
    html_file = response.text

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_file, 'lxml')
    # Get the containing tag
    container = soup.find('main', class_='content')

    # Get all articles as a list
    articles = container.find_all('article')
    # Looping through each article
    for article in articles:
        # Get article's title
        article_title = article.find('a', class_='entry-title-link').text
        # Get article's content
        article_content = article.find('div', class_='entry-content').p.text
        # Get Youtube's link
        try:
            article_iframe_link = article.find('div', class_='entry-content').span.iframe['src']
            article_link = get_ytb_link(article_iframe_link)
        except AttributeError:
            article_link = None
        return article_title, article_content, article_link


# Turn iframe youtube link to a normal one
def get_ytb_link(ytb_iframe_url):
    # Replace iframe youtube link with a normal youtube link using re's sub function
    replaced_url = re.sub(r'(embed/)', 'watch?v=', re.split(r'\?', ytb_iframe_url)[0])
    return replaced_url



# Main function
def main():
    # Create csv header
    with open('corey_scraped_data.csv', 'a') as new_file:
        # Create csv writer
        csv_reader = csv.DictReader(new_file)
        # Set csv titles
        field_names = ['Title', 'Content', 'Youtube link']
        # parse field_names in the new csv file
        csv_writer = csv.DictWriter(new_file, fieldnames=field_names)
        #
        csv_writer.writeheader()

        # Scrap Corey's blog
        for page_index in range(COREY_BLOG_PAGES_NUM):
            URL = f'https://coreyms.com/page/{page_index + 1}'
            # Get each scraped data as a tuple
            scraped_data = corey_blog_scraper(URL)
            # Get scraped data ready for csv parsing
            temp_dict = {'Title': scraped_data[0], 'Content': scraped_data[1], 'Youtube link': scraped_data[2]}
            # Parse temp_dict to the csv file
            csv_writer.writerow(temp_dict)
        print("Corey's blog successfully scraped.")


main()
