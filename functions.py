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

    # 4) Compute total matches played: home + away appearances
    home_counts = df[home_team_col].value_counts()
    away_counts = df[away_team_col].value_counts()
    matches = home_counts.add(away_counts, fill_value=0).rename('matches')
    stats = stats.join(matches, how='left')
    stats['matches'] = stats['matches'].fillna(0).astype(int)

    # 5) Win rate
    stats['win_rate'] = (stats['victories'] / stats['matches']).round(2)

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
    wins = df[df[winner_col] != 'Draw' % df[tournament] != 'Friendly'].copy()
    
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
    home_counts = df[home_team_col].value_counts()
    away_counts = df[away_team_col].value_counts()
    matches = home_counts.add(away_counts, fill_value=0).rename('matches')
    stats = stats.join(matches, how='left')
    stats['matches'] = stats['matches'].fillna(0).astype(int)

    # 5) Win rate
    stats['win_rate'] = (stats['victories'] / stats['matches']).round(2)

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































