import pandas as pd
import re
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm

tqdm.pandas()


def get_lon_lat_from_zip(df):
    df_copy = df.copy()
    geolocator = Nominatim(user_agent="my-application")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.1)
    # df['location'] = df['name'].apply(geocode)
    df_copy["location"] = df_copy["zip"].progress_apply(geocode)

    df_copy["point"] = df_copy["location"].apply(
        lambda loc: tuple(loc.point[:2]) if loc else None
    )
    return df_copy.drop(columns=["location"])


def aggregate_category_monthly(df, category="Engineer"):

    # filter category of jobs
    df = df[df["title"].progress_apply(lambda v: category in v)]

    df = df.dropna(subset=['city', 'created', 'delete_date'])
    # df = df.drop(columns=["last_checked", "last_updated", "ticke"])
    # df = df.dropna()
    find_year = lambda v: datetime.strptime(v.split('T')[0], '%Y-%m-%d').year
    # find_week = lambda v: int (datetime.strptime(str(v).split('T')[0], '%Y-%m-%d').strftime("%V"))

    find_month = lambda v: int (datetime.strptime(str(v).split('T')[0], '%Y-%m-%d').month)
    find_region = lambda v: re.split('\d+', v)[0]

    # df["created"] = df["created"].apply(lambda v: v[:10])
    # df["delete_date"] = df["delete_date"].apply(lambda v: v[:10])
    df["year"] = df["created"].progress_apply(find_year)
    df["start_week"] = df["created"].progress_apply(find_month)
    df["end_week"] = df["delete_date"].progress_apply(find_month)
    # df["county_zip"] = df["zip"].progress_apply(find_region)

    year_min = df["year"].min()
    year_max = df["year"].max()
    week_min = df["start_week"].min()
    week_max = df["start_week"].max()

    # find interval weekly of each job
    df_aggregate = pd.DataFrame(columns=["year", "week", "num_jobs", "city"])
    cities = df["city"].unique().tolist()

    print("Aggregating over {}".format(df.shape))

    # find if (week, year) is contained in region
    for year in tqdm(range(year_min, year_max + 1)):
        for week in range(week_min, week_max + 1):
            for city in cities:
                index = (
                    (df["start_week"] <= week)
                    & (week <= df["end_week"])
                    & (df["year"] == year)
                    & (df["city"] == city)
                )
                num_jobs = sum(index)
                df_tmp = pd.DataFrame(
                    {"year": [year], "week": [week], "num_jobs": [num_jobs], "city":[city]}
                )
                df_aggregate = df_aggregate.append(df_tmp)
    return df_aggregate

    ## if yes how many and keep indexes as dict

def county_referedum_table(euro_referendum_result, town_list):
    """ run by 
        county_referedum_table("clean_data/euro_referendum_result.csv", "clean_data/Towns_List.csv")
    """
    df_referendum = pd.read_csv(euro_referendum_result)
    df_town = pd.read_csv(town_list)
    df_tmp= df_town.merge(df_referendum[["Area","Pct_Remain","Pct_Leave","Pct_Rejected"]], left_on='Town', right_on='Area' ).groupby("County")
    df_county = pd.core.groupby.generic.DataFrameGroupBy.mean(df_tmp)
    return df_town.merge(df_county, left_on='County', right_on='County' )
    