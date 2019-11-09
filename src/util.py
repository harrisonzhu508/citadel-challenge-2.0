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
    df_copy["location"] = df_copy["zip"].progress_apply(geocode)

    df_copy["point"] = df_copy["location"].apply(
        lambda loc: tuple(loc.point[:2]) if loc else None
    )
    return df_copy.drop(columns=["location"])


def aggregate_category_monthly(df, category="Engineer"):

    find_year = lambda v: datetime.date(
        int(v[:4]), int(v[5:7]), int(v[8:])
    ).isocalendar()[0]
    find_week = lambda v: datetime.date(
        int(v[:4]), int(v[5:7]), int(v[8:])
    ).isocalendar()[1]

    df["created"] = df["created"].apply(lambda v: v[:10])
    df["delete_date"] = df["delete_date"].apply(lambda v: v[:10])
    df["year"] = df["created"].apply(find_year)
    df["start_week"] = df["created"].apply(find_week)
    df["end_week"] = df["delete_date"].apply(find_week)

    year_min = df["year"].min()
    year_max = df["year"].max()
    week_min = df["start_week"].min()
    week_max = df["start_week"].max()

    # filter category of jobs
    df = df[df["title"].apply(lambda v: category in v)]

    # find interval weekly of each job
    df_aggregate = pd.DataFrame(columns=["year", "week", "num_jobs"])

    # find if (week, year) is contained in region
    for year in range(year_min, year_max + 1):
        for week in range(week_min, week_max + 1):
            index = (
                (df["start_week"] <= week)
                & (week <= df["end_week"])
                & (df["year"] == year)
            )
            num_jobs = sum(index)
            df_tmp = pd.DataFrame(
                {"year": [year], "week": [week], "num_jobs": [num_jobs]}
            )
            df_aggregate = df_aggregate.append(df_tmp)

    return df_aggregate

    ## if yes how many and keep indexes as dict

