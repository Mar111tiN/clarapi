from datetime import date as dt
import os
import re
import pandas as pd
from tables import Image, Collection, User, Keyword

title_pat = re.compile(r'^\w')

months = ['jan', 'feb', 'mär', 'apr', 'mai', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dez']
month_dict = {month[1]:month[0] + 1 for month in enumerate(months)}

def str2date(string):
    if pd.isnull(string) or string == '?':
        return dt(2018, 1,1)
    if '.' in string:
        data = [int(num) for num in string.split('.')]
        return dt(data[2], data[1], data[0])
        
    date = string.split(' ')
    year = int(date[-1])
    year = 2000 + year if (year < 2000) else year
    month = date[0][:3].lower() if (len(date) - 1) else 'jan'
    month = month_dict[month] if month in month_dict.keys() else 1
    return dt(year, month, 1)

def add2db(row, session=False, pix_path="."):
    '''
    adds rows from the df to the database
    '''
    
    # file and file check
    pix_file = f"Clara{str(row['img # ']).zfill(4)}.jpg"
    # file path relative to database location
    pix_file_abs = os.path.join(pix_path, pix_file)
    if not os.path.isfile(pix_file_abs):
        return f'File {pix_file} does not exist'
    title = row['Title'] if row['Title'] == row['Title'] else 'ohne Titel'
    if not title_pat.match(title):
        title = 'ohne Titel'
        

    name = row['Wer'] if pd.notnull(row['Wer']) else 'Clara'
    stars = 0
    
    # if user exists, use this user
    artist = session.query(User).filter_by(name = name).first()
    # else create new user/artist
    if not artist:
        artist = User(name=name, age=6)
    
    # check if image already exists in db
    image = session.query(Image).filter_by(title=title).filter_by(path=pix_file_abs).first()
    if image:
        return f'Image {image.title} exists!'
    # create image instance
    image = Image(title=title, path=pix_file_abs, artist=artist, note=row['Note'], date=str2date(row['Datum']))

    if pd.notnull(row['Set']):
        collection = session.query(Collection).filter_by(name = row['Set']).first()
        if not collection:
            collection = Collection(name=row['Set'])
        image.collection = collection
        
    def get_key(key):
        keyword = session.query(Keyword).filter_by(name = key.strip()).first()
        keyword = keyword if keyword else Keyword(name=key.strip())
        return keyword
    
    if pd.notnull(row['Key']):
        image.keywords = [get_key(key) for key in row['Key'].split(',')]
    if pd.notnull(row['Hilfe von']):
        image.helper = row['Hilfe von']
    date_assumed = row['Datum unbekannt'] in ['x',''] or (row['Datum'] in ['', '?'])
    image.date_assumed = date_assumed
    session.add(image)
    return repr(image)