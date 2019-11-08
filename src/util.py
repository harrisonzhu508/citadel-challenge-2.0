import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm
tqdm.pandas()

def get_lon_lat_from_zip(df):
    df_copy = df.copy()
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.1)
    # df['location'] = df['name'].apply(geocode)
    df_copy['location'] = df_copy['zip'].progress_apply(geocode)

    df_copy['point'] = df_copy['location'].apply(lambda loc: tuple(loc.point[:2]) if loc else None)
    return df_copy.drop(columns = ['location'])