import pandas as pd

# 1. Load mock data with semicolon separator
df_mock = pd.read_csv(r"C:\Users\pytho\Documents\nhl\mock.csv", sep=';')

# Clean accidental quote properties from column names if present
df_mock.columns = [col.replace('"', '') for col in df_mock.columns]

# 2. Load the target historical odds file
df_odds = pd.read_csv(r"C:\Users\pytho\Documents\nhl\nhl_historical_odds_2018_2019.csv")

# 3. Create a standardized string date column inside the odds table
df_odds['date'] = pd.to_datetime(df_odds['timestamp'], unit='s', utc=True).dt.strftime('%Y-%m-%d')

# 4. Split the single combined match name column into absolute strings
df_odds[['odds_home', 'odds_away']] = df_odds['match'].str.split(' - ', expand=True)
df_odds['odds_home'] = df_odds['odds_home'].str.strip()
df_odds['odds_away'] = df_odds['odds_away'].str.strip()

# 5. Build an automated nickname-to-fullname dictionary index
odds_unique_teams = set(df_odds['odds_home'].unique()).union(set(df_odds['odds_away'].unique()))
mock_unique_teams = df_mock['home_team'].unique()

nickname_to_full = {}
for mock_team in mock_unique_teams:
    for odds_team in odds_unique_teams:
        if mock_team in odds_team:
            nickname_to_full[mock_team] = odds_team
            break

# Map your short nicknames inside mock dataset out to match full system names
df_mock['full_home'] = df_mock['home_team'].map(nickname_to_full)
df_mock['full_away'] = df_mock['away_team'].map(nickname_to_full)

# 6. Filter and rename metrics to match requirements
df_odds_subset = df_odds[['date', 'odds_home', 'odds_away', 'time', 'odds_1', 'odds_x', 'odds_2']].rename(
    columns={'odds_2': 'odds_y', 'odds_home': 'full_home', 'odds_away': 'full_away'}
)

# 7. Merge tables on Shared Date, Home Team ID, and Away Team ID configurations
final_mock_merged = pd.merge(
    df_mock,
    df_odds_subset,
    on=['date', 'full_home', 'full_away'],
    how='inner'
)

# 8. Drop structural validation tracking helpers
final_mock_merged = final_mock_merged.drop(columns=['full_home', 'full_away'])

final_mock_merged.to_csv("merged_mock_and_odds.csv", index=False)

print("Successfully merged datasets!")
print("Columns in final output:", final_mock_merged.columns.tolist())