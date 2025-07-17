import pandas as pd

def df_20_total(df,winner_col = "winner", away_score_col = 'away_score', home_score_col = 'home_score', away_team_col = 'away_team', home_team_col = 'home_team'):
    
    # 1) Filter out draws to get only wins for victory counts
    wins = df[df[winner_col] != 'Draw'].copy()
    
    # 2) Flag home vs away wins
    wins['home_win'] = wins[winner_col] == wins[home_team_col]
    wins['away_win'] = wins[winner_col] == wins[away_team_col]

    # 3) Aggregate win stats by team
    stats = wins.groupby(winner_col).agg(
        victories       = (winner_col,  'size'),
        home_victories  = ('home_win',  'sum'),
        away_victories  = ('away_win',  'sum')
    )

    # 4) Compute total matches played: home, draws + away appearances
    home_counts = df['home_team'].value_counts()
    away_counts = df['away_team'].value_counts()
    matches = home_counts.add(away_counts, fill_value=0).rename('matches')
    
    stats = stats.join(matches, how='left')
    stats['matches'] = stats['matches'].fillna(0).astype(int)

    # 5) Win rate
    stats['win_rate'] = (stats['victories'] / stats['matches']) \
                   .map("{:.2%}".format)

    # 6) Compute total goals scored in all matches
    goals_home = df.groupby(home_team_col)[home_score_col].sum()
    goals_away = df.groupby(away_team_col)[away_score_col].sum()
    total_goals = goals_home.add(goals_away, fill_value=0).rename('total_goals')
    stats = stats.join(total_goals, how='left')
    stats['total_goals'] = stats['total_goals'].fillna(0).astype(int)

    # 7) Average goals per match
    stats['avg_goals_per_match'] = (stats['total_goals'] / stats['matches']).round(2)

    # 8) Sort by victories and take top 20
    top20 = stats.sort_values('victories', ascending=False).head(20)

    # 9) Ensure column order
    cols = [
        'matches', 'victories', 'home_victories', 'away_victories',
        'total_goals', 'avg_goals_per_match', 'win_rate'
    ]
    return top20[cols]


def df_20_off(df,winner_col = "winner", away_score_col = 'away_score', home_score_col = 'home_score', away_team_col = 'away_team', home_team_col = 'home_team', tournament = 'tournament'):
    
    # 1) Filter out draws and friendly to get only wins for victory counts
    wins = df[(df[winner_col] != 'Draw') & (df[tournament]    != 'Friendly')].copy()
    
    # 2) Flag home vs away wins
    wins['home_win'] = wins[winner_col] == wins[home_team_col]
    wins['away_win'] = wins[winner_col] == wins[away_team_col]

    # 3) Aggregate win stats by team
    stats = wins.groupby(winner_col).agg(
        victories       = (winner_col,  'size'),
        home_victories  = ('home_win',  'sum'),
        away_victories  = ('away_win',  'sum')
    )

    # 4) Compute total matches played: home + away appearances
    non_friendly = df[df['tournament'] != 'Friendly']
    home_counts = non_friendly['home_team'].value_counts()
    away_counts = non_friendly['away_team'].value_counts()
    matches = home_counts.add(away_counts, fill_value=0).rename('matches')
    stats = stats.join(matches, how='left')
    stats['matches'] = stats['matches'].fillna(0).astype(int)

    # 5) Win rate
    stats['win_rate'] = (stats['victories'] / stats['matches']) \
                   .map("{:.2%}".format)

    # 6) Compute total goals scored in all matches
    goals_home = non_friendly.groupby(home_team_col)[home_score_col].sum()
    goals_away = non_friendly.groupby(away_team_col)[away_score_col].sum()
    total_goals = goals_home.add(goals_away, fill_value=0).rename('total_goals')
    stats = stats.join(total_goals, how='left')
    stats['total_goals'] = stats['total_goals'].fillna(0).astype(int)

    # 7) Average goals per match
    stats['avg_goals_per_match'] = (stats['total_goals'] / stats['matches']).round(2)

    # 8) Sort by victories and take top 20
    top20 = stats.sort_values('victories', ascending=False).head(20)

    # 9) Ensure column order
    cols = [
        'matches', 'victories', 'home_victories', 'away_victories',
        'total_goals', 'avg_goals_per_match', 'win_rate'
    ]
    return top20[cols] 


def df_20_world_cup(df,winner_col = "winner", away_score_col = 'away_score', home_score_col = 'home_score', away_team_col = 'away_team', home_team_col = 'home_team', tournament = 'tournament'):
    
    # 1) Filter out draws and friendly to get only wins for victory counts
    wins = df[(df[winner_col] != 'Draw') & (df[tournament] == 'FIFA World Cup')].copy()
    
    # 2) Flag home vs away wins
    wins['home_win'] = wins[winner_col] == wins[home_team_col]
    wins['away_win'] = wins[winner_col] == wins[away_team_col]

    # 3) Aggregate win stats by team
    stats = wins.groupby(winner_col).agg(
        victories       = (winner_col,  'size'),
        home_victories  = ('home_win',  'sum'),
        away_victories  = ('away_win',  'sum')
    )

    # 4) Compute total matches played: home + away appearances
    worldcup = df[df['tournament'] == 'FIFA World Cup']
    home_counts = worldcup['home_team'].value_counts()
    away_counts = worldcup['away_team'].value_counts()
    matches = home_counts.add(away_counts, fill_value=0).rename('matches')
    stats = stats.join(matches, how='left')
    stats['matches'] = stats['matches'].fillna(0).astype(int)

    # 5) Win rate
    stats['win_rate'] = (stats['victories'] / stats['matches']) \
                   .map("{:.2%}".format)

    # 6) Compute total goals scored in all matches
    goals_home = worldcup.groupby(home_team_col)[home_score_col].sum()
    goals_away = worldcup.groupby(away_team_col)[away_score_col].sum()
    total_goals = goals_home.add(goals_away, fill_value=0).rename('total_goals')
    stats = stats.join(total_goals, how='left')
    stats['total_goals'] = stats['total_goals'].fillna(0).astype(int)

    # 7) Average goals per match
    stats['avg_goals_per_match'] = (stats['total_goals'] / stats['matches']).round(2)

    # 8) Sort by victories and take top 20
    top20 = stats.sort_values('victories', ascending=False).head(20)

    # 9) Ensure column order
    cols = [
        'matches', 'victories', 'home_victories', 'away_victories',
        'total_goals', 'avg_goals_per_match', 'win_rate'
    ]
    return top20[cols] 



def top5_off_by_continent(
      df,
    winner_col         = "winner",
    away_score_col     = 'away_score',
    home_score_col     = 'home_score',
    away_team_col      = 'away_team',
    home_team_col      = 'home_team',
    tournament         = 'tournament'
):
    # 1) Filter out draws and friendlies for victory counts
    wins = df[(df[winner_col] != 'Draw') & (df[tournament] != 'Friendly')].copy()
    # 2) Flag home vs away
    wins['home_win'] = wins[winner_col] == wins[home_team_col]
    wins['away_win'] = wins[winner_col] == wins[away_team_col]
    # 3) Aggregate wins
    stats = wins.groupby(winner_col).agg(
        victories       = (winner_col, 'size'),
        home_victories  = ('home_win', 'sum'),
        away_victories  = ('away_win', 'sum')
    )
    # 4) Count non-friendly matches for matches played
    non_friendly = df[df[tournament] != 'Friendly']
    home_counts   = non_friendly[home_team_col].value_counts()
    away_counts   = non_friendly[away_team_col].value_counts()
    matches       = home_counts.add(away_counts, fill_value=0).rename('matches')
    stats         = stats.join(matches, how='left').fillna({'matches':0}).astype({'matches':int})
    # 5) Win rate
    stats['win_rate'] = (stats['victories'] / stats['matches']).map('{:.2%}'.format)
    # 6) Total goals
    goals_home  = non_friendly.groupby(home_team_col)[home_score_col].sum()
    goals_away  = non_friendly.groupby(away_team_col)[away_score_col].sum()
    total_goals = goals_home.add(goals_away, fill_value=0).rename('total_goals')
    stats       = stats.join(total_goals, how='left').fillna({'total_goals':0}).astype({'total_goals':int})
    # 7) Avg goals
    stats['avg_goals_per_match'] = (stats['total_goals'] / stats['matches']).round(2)
   
    # 9) Return 5 winners per continent
    continent_map = { 'Tunisia':'Africa','Ukraine':'Europe', 'South Korea':'Asia','Brazil':'America','Argentina':'America','Chile':'America','Colombia':'America','Costa Rica':'America','Cuba':'America','Dominican Republic':'America','Ecuador':'America','El Salvador':'America','Guatemala':'America','Haiti':'America','Honduras':'America','Jamaica':'America','Mexico':'America','Panama':'America','Paraguay':'America','Peru':'America','Trinidad and Tobago':'America','United States':'America','Uruguay':'America','Venezuela':'America','Bolivia':'America','Canada':'America','Guyana':'America','Suriname':'America','Bahamas':'America','Barbados':'America','Belize':'America','Grenada':'America','Saint Lucia':'America','Saint Vincent and the Grenadines':'America','Antigua and Barbuda':'America','Dominica':'America','Saint Kitts and Nevis':'America','Puerto Rico':'America','Aruba':'America','Bermuda':'America','French Guiana':'America','Martinique':'America','Algeria':'Africa','Angola':'Africa','Benin':'Africa','Botswana':'Africa','Burkina Faso':'Africa','Burundi':'Africa','Cameroon':'Africa','Cape Verde':'Africa','Central African Republic':'Africa','Chad':'Africa','Comoros':'Africa','Congo':'Africa','DR Congo':'Africa','Côte d\'Ivoire':'Africa','Equatorial Guinea':'Africa','Eswatini':'Africa','Ethiopia':'Africa','Gabon':'Africa','Gambia':'Africa','Ghana':'Africa','Guinea':'Africa','Guinea-Bissau':'Africa','Kenya':'Africa','Lesotho':'Africa','Liberia':'Africa','Libya':'Africa','Madagascar':'Africa','Malawi':'Africa','Mauritania':'Africa','Mauritius':'Africa','Morocco':'Africa','Mozambique':'Africa','Namibia':'Africa','Niger':'Africa','Nigeria':'Africa','Rwanda':'Africa','Senegal':'Africa','Seychelles':'Africa','Sierra Leone':'Africa','South Africa':'Africa','Sudan':'Africa','Tanzania':'Africa','Togo':'Africa','Uganda':'Africa','Zambia':'Africa','Zimbabwe':'Africa','Guadeloupe':'America','Curaçao':'America','Germany':'Europe','France':'Europe','Italy':'Europe','Spain':'Europe','England':'Europe','Scotland':'Europe','Wales':'Europe','Northern Ireland':'Europe','Netherlands':'Europe','Belgium':'Europe','Portugal':'Europe','Russia':'Europe','Sweden':'Europe','Norway':'Europe','Denmark':'Europe','Finland':'Europe','Poland':'Europe','Austria':'Europe','Greece':'Europe','Czech Republic':'Europe','Slovakia':'Europe','Hungary':'Europe','Romania':'Europe','Croatia':'Europe','Serbia':'Europe','Slovenia':'Europe','Bosnia and Herzegovina':'Europe','Albania':'Europe','North Macedonia':'Europe','Montenegro':'Europe','Belarus':'Europe','Lithuania':'Europe','Latvia':'Europe','Estonia':'Europe','Iceland':'Europe','Ireland':'Europe','Luxembourg':'Europe','Malta':'Europe','Cyprus':'Europe','Andorra':'Europe','Armenia':'Europe','Azerbaijan':'Europe','Georgia':'Europe','Liechtenstein':'Europe','San Marino':'Europe','Vatican City':'Europe','Alderney':'Europe','Bulgaria':'Europe','Czechoslovakia':'Europe','German DR':'Europe','Gibraltar':'Europe','Guernsey':'Europe','Jersey':'Europe','Republic of Ireland':'Europe','Switzerland':'Europe','Faroe Islands':'Europe','Yugoslavia':'Europe','Afghanistan':'Asia','Bangladesh':'Asia','Brunei':'Asia','Cambodia':'Asia','China PR':'Asia','India':'Asia','Indonesia':'Asia','Iran':'Asia','Iraq':'Asia','Israel':'Asia','Japan':'Asia','Jordan':'Asia','Kazakhstan':'Asia','Kuwait':'Asia','Kyrgyzstan':'Asia','Laos':'Asia','Lebanon':'Asia','Macau':'Asia','Maldives':'Asia','Myanmar':'Asia','Nepal':'Asia','North Korea':'Asia','Oman':'Asia','Pakistan':'Asia','Palestine':'Asia','Philippines':'Asia','Qatar':'Asia','Saudi Arabia':'Asia','Singapore':'Asia','Sri Lanka':'Asia','Syria':'Asia','Taiwan':'Asia','Tajikistan':'Asia','Thailand':'Asia','Turkey':'Europe','Turkmenistan':'Asia','United Arab Emirates':'Asia','Uzbekistan':'Asia','Vietnam':'Asia','Vietnam Republic':'Asia','Yemen':'Asia','Australia':'Oceania','New Zealand':'Oceania','Fiji':'Oceania','New Caledonia':'Oceania','Papua New Guinea':'Oceania','Solomon Islands':'Oceania','Tahiti':'Oceania','Vanuatu':'Oceania' , 'Egypt':'Africa','Ivory Coast':'Africa','Moldova':'Europe' , 'Bahrain':'Asia','Hong Kong':'Asia','Malaysia':'Asia','Mali':'Africa'}

    # Map each winner to continent
    df_out = stats.reset_index().rename(columns={winner_col:'team'})
    df_out['continent'] = df_out['team'].map(continent_map)
    result = (
        df_out.sort_values(['continent','victories'], ascending=[True,False])
              .groupby('continent', group_keys=False)
              .head(5)
              .set_index(['continent','team'])
    )
    return result

def top5_worldcup_by_continent(
          df,
    winner_col         = "winner",
    away_score_col     = 'away_score',
    home_score_col     = 'home_score',
    away_team_col      = 'away_team',
    home_team_col      = 'home_team',
    tournament         = 'tournament'
):
    # 1) Filter out draws and friendlies for victory counts
    wins = df[(df[winner_col] != 'Draw') & (df[tournament] == 'FIFA World Cup')].copy()
    # 2) Flag home vs away
    wins['home_win'] = wins[winner_col] == wins[home_team_col]
    wins['away_win'] = wins[winner_col] == wins[away_team_col]
    # 3) Aggregate wins
    stats = wins.groupby(winner_col).agg(
        victories       = (winner_col, 'size'),
        home_victories  = ('home_win', 'sum'),
        away_victories  = ('away_win', 'sum')
    )
    # 4) Count non-friendly matches for matches played
    worldcup = df[df['tournament'] == 'FIFA World Cup']
    home_counts = worldcup['home_team'].value_counts()
    away_counts = worldcup['away_team'].value_counts()
    matches       = home_counts.add(away_counts, fill_value=0).rename('matches')
    stats         = stats.join(matches, how='left').fillna({'matches':0}).astype({'matches':int})
    # 5) Win rate
    stats['win_rate'] = (stats['victories'] / stats['matches']).map('{:.2%}'.format)
    # 6) Total goals
    goals_home  = worldcup.groupby(home_team_col)[home_score_col].sum()
    goals_away  = worldcup.groupby(away_team_col)[away_score_col].sum()
    total_goals = goals_home.add(goals_away, fill_value=0).rename('total_goals')
    stats       = stats.join(total_goals, how='left').fillna({'total_goals':0}).astype({'total_goals':int})
    # 7) Avg goals
    stats['avg_goals_per_match'] = (stats['total_goals'] / stats['matches']).round(2)
    
    # 9) Return 5 winners per continent
    continent_map = { 'Tunisia':'Africa','Ukraine':'Europe', 'South Korea':'Asia','Brazil':'America','Argentina':'America','Chile':'America','Colombia':'America','Costa Rica':'America','Cuba':'America','Dominican Republic':'America','Ecuador':'America','El Salvador':'America','Guatemala':'America','Haiti':'America','Honduras':'America','Jamaica':'America','Mexico':'America','Panama':'America','Paraguay':'America','Peru':'America','Trinidad and Tobago':'America','United States':'America','Uruguay':'America','Venezuela':'America','Bolivia':'America','Canada':'America','Guyana':'America','Suriname':'America','Bahamas':'America','Barbados':'America','Belize':'America','Grenada':'America','Saint Lucia':'America','Saint Vincent and the Grenadines':'America','Antigua and Barbuda':'America','Dominica':'America','Saint Kitts and Nevis':'America','Puerto Rico':'America','Aruba':'America','Bermuda':'America','French Guiana':'America','Martinique':'America','Algeria':'Africa','Angola':'Africa','Benin':'Africa','Botswana':'Africa','Burkina Faso':'Africa','Burundi':'Africa','Cameroon':'Africa','Cape Verde':'Africa','Central African Republic':'Africa','Chad':'Africa','Comoros':'Africa','Congo':'Africa','DR Congo':'Africa','Côte d\'Ivoire':'Africa','Equatorial Guinea':'Africa','Eswatini':'Africa','Ethiopia':'Africa','Gabon':'Africa','Gambia':'Africa','Ghana':'Africa','Guinea':'Africa','Guinea-Bissau':'Africa','Kenya':'Africa','Lesotho':'Africa','Liberia':'Africa','Libya':'Africa','Madagascar':'Africa','Malawi':'Africa','Mauritania':'Africa','Mauritius':'Africa','Morocco':'Africa','Mozambique':'Africa','Namibia':'Africa','Niger':'Africa','Nigeria':'Africa','Rwanda':'Africa','Senegal':'Africa','Seychelles':'Africa','Sierra Leone':'Africa','South Africa':'Africa','Sudan':'Africa','Tanzania':'Africa','Togo':'Africa','Uganda':'Africa','Zambia':'Africa','Zimbabwe':'Africa','Guadeloupe':'America','Curaçao':'America','Germany':'Europe','France':'Europe','Italy':'Europe','Spain':'Europe','England':'Europe','Scotland':'Europe','Wales':'Europe','Northern Ireland':'Europe','Netherlands':'Europe','Belgium':'Europe','Portugal':'Europe','Russia':'Europe','Sweden':'Europe','Norway':'Europe','Denmark':'Europe','Finland':'Europe','Poland':'Europe','Austria':'Europe','Greece':'Europe','Czech Republic':'Europe','Slovakia':'Europe','Hungary':'Europe','Romania':'Europe','Croatia':'Europe','Serbia':'Europe','Slovenia':'Europe','Bosnia and Herzegovina':'Europe','Albania':'Europe','North Macedonia':'Europe','Montenegro':'Europe','Belarus':'Europe','Lithuania':'Europe','Latvia':'Europe','Estonia':'Europe','Iceland':'Europe','Ireland':'Europe','Luxembourg':'Europe','Malta':'Europe','Cyprus':'Europe','Andorra':'Europe','Armenia':'Europe','Azerbaijan':'Europe','Georgia':'Europe','Liechtenstein':'Europe','San Marino':'Europe','Vatican City':'Europe','Alderney':'Europe','Bulgaria':'Europe','Czechoslovakia':'Europe','German DR':'Europe','Gibraltar':'Europe','Guernsey':'Europe','Jersey':'Europe','Republic of Ireland':'Europe','Switzerland':'Europe','Faroe Islands':'Europe','Yugoslavia':'Europe','Afghanistan':'Asia','Bangladesh':'Asia','Brunei':'Asia','Cambodia':'Asia','China PR':'Asia','India':'Asia','Indonesia':'Asia','Iran':'Asia','Iraq':'Asia','Israel':'Asia','Japan':'Asia','Jordan':'Asia','Kazakhstan':'Asia','Kuwait':'Asia','Kyrgyzstan':'Asia','Laos':'Asia','Lebanon':'Asia','Macau':'Asia','Maldives':'Asia','Myanmar':'Asia','Nepal':'Asia','North Korea':'Asia','Oman':'Asia','Pakistan':'Asia','Palestine':'Asia','Philippines':'Asia','Qatar':'Asia','Saudi Arabia':'Asia','Singapore':'Asia','Sri Lanka':'Asia','Syria':'Asia','Taiwan':'Asia','Tajikistan':'Asia','Thailand':'Asia','Turkey':'Europe','Turkmenistan':'Asia','United Arab Emirates':'Asia','Uzbekistan':'Asia','Vietnam':'Asia','Vietnam Republic':'Asia','Yemen':'Asia','Australia':'Oceania','New Zealand':'Oceania','Fiji':'Oceania','New Caledonia':'Oceania','Papua New Guinea':'Oceania','Solomon Islands':'Oceania','Tahiti':'Oceania','Vanuatu':'Oceania' , 'Egypt':'Africa','Ivory Coast':'Africa','Moldova':'Europe' , 'Bahrain':'Asia','Hong Kong':'Asia','Malaysia':'Asia','Mali':'Africa'}

    # Map each winner to continent
    df_out = stats.reset_index().rename(columns={winner_col:'team'})
    df_out['continent'] = df_out['team'].map(continent_map)
    result = (
        df_out.sort_values(['continent','victories'], ascending=[True,False])
              .groupby('continent', group_keys=False)
              .head(5)
              .set_index(['continent','team'])
    )
    return result























