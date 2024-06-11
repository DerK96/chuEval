import cartopy
from pprint import pprint
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path

if __name__ == '__main__':
    print("Start")

    season = "23_24"

    mainPath = Path(f"/home/flippi/Desktop/Saison_{season}")
    print(mainPath)

    visitFilename = "VisitList.csv"

    dataPath = mainPath / 'htmlOutput'

    df = pd.read_csv(dataPath / visitFilename)
    pprint(df)

    print(df.columns)

    print(np.mean(df.loc[:, 'nrchu']))
    print(np.median(df.loc[:, 'nrchu']))

    gerPath = Path("/home/flippi/Desktop/Saison_23_24/de_1.csv")

    ger = pd.read_csv(gerPath)
    print(ger.head())

    merged_df = pd.merge(df, ger[['city', 'lat', 'lng']], left_on='origin', right_on='city', how='inner')

    pprint(merged_df)

    fig = plt.figure(figsize=(8.27, 11.69))
    ax = plt.axes(projection=cartopy.crs.UTM(32))
    ax.set_extent([5.5, 15.5, 47, 55])
    ax.add_feature(cartopy.feature.BORDERS, edgecolor='gray')
    ax.add_feature(cartopy.feature.COASTLINE, edgecolor='gray')

    cnt = 0
    for index, row in merged_df.iterrows():
        origin_city = row['origin']
        lat = row['lat']
        lng = row['lng']
        print(f"{origin_city}: ({lat}, {lng})")
        ax.plot(lng, lat, 's', ms=2, c="#000000", transform=cartopy.crs.PlateCarree())
        cnt += 1

    print(f"Nr of Cities: {cnt}")

    # create an empty dictionary to store the latitude and longitude values for each destination column
    dest_lat_lon_dict = {}

    # iterate over the destination columns in df1 and perform a left join with df2 for each column
    for col in df.filter(like='visit').columns:
        # perform a left join between df1 and df2 on the destination column and the 'city' column
        merged_df = pd.merge(df, ger[['city', 'lat', 'lng']], left_on=col, right_on='city', how='left')
        # group the merged dataframe by 'origin' and extract the 'lat' and 'lon' values for each group
        grouped_df = merged_df.groupby('origin')[['lat', 'lng']].agg(list)
        # store the 'lat' and 'lon' lists in the dictionary with the column name as the key
        dest_lat_lon_dict[col] = [list(zip(lat, lng)) for lat, lng in grouped_df.values]

    # create a new column in df1 for each destination column containing the 'lat' and 'lon' lists for each origin
    for col, lat_lon_list in dest_lat_lon_dict.items():
        df[col + '_lat_lng'] = lat_lon_list

    pprint(df)
    df.to_csv(f"./eval_{season}.csv")
    # create a dictionary that maps each origin to a unique color
    origins = merged_df['origin'].unique()
    color_map = plt.cm.get_cmap('tab20', len(origins))

    # iterate over the 'visitX_lat_lon' columns that are not NaN for each origin
    for col in df.filter(like='visit').columns:
        col_lat_lon = col + '_lat_lng'
        if col_lat_lon in df.columns:
            for i, row in df[df[col + '_lat_lng'].notnull()].iterrows():
                origin_city = row['origin']
                # print(origin_city)
                color = color_map(i % len(origins))
                if len(ger.loc[ger['city'] == origin_city, ['lat', 'lng']]) > 0:
                    origin_lat, origin_lon = ger.loc[ger['city'] == origin_city, ['lat', 'lng']].iloc[0]
                    for dest_lat, dest_lon in row[col + '_lat_lng']:
                        ax.plot([origin_lon, dest_lon], [origin_lat, dest_lat], c=color, linewidth=0.5,
                                transform=cartopy.crs.PlateCarree())
        else:
            print(f"{col_lat_lon} not found in df.columns")

    plt.title(f"Saison: {season}")
    fig.savefig(f'visits_{season}.jpg', dpi=300)

    # plt.show()
    plt.close(fig)
