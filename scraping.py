from bs4 import BeautifulSoup
import requests
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import datetime
from gspread_dataframe import set_with_dataframe

def get_data_u():
    url = 'https://scraping-for-beginner.herokuapp.com/udemy'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    n_subscriber = soup.find('p', {'class': 'subscribers'}).text
    n_subscriber = int(n_subscriber.split('：')[1])

    n_review = soup.find('p', {'class': 'reviews'}).text
    n_review = int(n_review.split('：')[1])
    return{
        'n_subscriber': n_subscriber,
        'n_review': n_review
    }

def main():
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    credentials = Credentials.from_service_account_file(
        'service_account.json',
        scopes=scopes
    )

    gc = gspread.authorize(credentials)

    SP_SHEET_KEY = '165NODVzBD2zQKhDQEz5YPbB5COufnV6ApTQwleOaGUc'
    sh = gc.open_by_key(SP_SHEET_KEY)

    SP_SHEET = 'db'
    worksheet = sh.worksheet(SP_SHEET)

    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])

    data_u = get_data_u()
    today = datetime.date.today().strftime('%Y/%m/%d')

    data_u['date'] = today
    df = df.append(data_u, ignore_index=True)

    set_with_dataframe(worksheet, df, row=1, col=1)

if __name__ == '__main__':
    main()