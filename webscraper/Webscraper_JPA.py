import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

## Print Statements
VERBOSE = True

## File Destinations
save_dir = "webscraper/data_webscraping"
os.makedirs(save_dir, exist_ok=True)

save_path_concert_dates = os.path.join(save_dir, "Webscraper_BS_PD.csv")
save_path_teilnahmebedingungen = os.path.join(save_dir, "JPA_Teilnahmebedingungen.pdf")

## Load the webpage
def load_http(url):
    ''' Load the webpage of a given URL via http request and returns the content parsed by BeautifulSoup.'''
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
    except requests.exceptions.HTTPError as err:
        print('HTTP error occurred:', err)
    except Exception as err:
        print('Other error occurred:', err)

    # Parse and return the HTML content
    return BeautifulSoup(response.content, 'html.parser')

def download_doc(url, save_path):
    document_response = requests.get(url)

    if document_response.status_code == 200:
        # Save the document to a file
        with open(save_path, 'wb') as file:
            file.write(document_response.content)
        print('Document downloaded successfully.')
    else:
        print('Failed to download the document. Status code:', document_response.status_code)

def extract_JPA_concert_dates():
    ''' Extracts the concert dates of the "Junge Philharmonie Augsburg" from their webpage.'''
    url = 'https://musikfreizeit.de/'
    soup = load_http(url)
    
    # Find the last table containing the concert dates
    tables = soup.find_all("table")
    last_table = tables[-1]

    # Extract table rows and their text
    data = []
    rows = last_table.find_all("tr")
    for row in rows:
        cells = row.find_all(["td", "th"])
        text = [cell.get_text(strip=True) for cell in cells]
        if text:    # Skips empty rows
            data.append(text)

    # Print the concerts
    if VERBOSE:
        for concert in data:
            print(" | ".join(concert)) # joins all strings in concert with " | " as separator

    # Convert the data into a pandas DataFrame for easier manipulation
    df = pd.DataFrame(data, columns=['Date', 'Location', 'Time'])

    # Save the DataFrame to a CSV file
    df.to_csv(save_path_concert_dates)
    print('Data successfully saved to Webscraper_BS_PD.csv')

def download_PDF():
    url = "https://musikfreizeit.de/anmeldung-musikfreizeit/"
    soup = load_http(url)

    # Find all <a> tags
    links = soup.find_all("a")

    # Extract and print href attributes
    for link in links:
        href = link.get("href")
        if "teilnahmebedingungen" in href.lower():
            # Download the document and exit
            download_doc(href, save_path_teilnahmebedingungen)
            break

extract_JPA_concert_dates()
download_PDF()