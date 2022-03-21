"""Contains data in support of a fantasy baseball client application.
"""


team_abbrev = {
    'Diamondbacks': 'ARI',
    'Braves': 'ATL',
    'Orioles': 'BAL',
    'Red Sox': 'BOS',
    'Cubs': 'CHC',
    'White Sox': 'CHW',
    'Reds': 'CIN',
    'Indians': 'CLE',
    'Rockies': 'COL',
    'Tigers': 'DET',
    'Astros': 'HOU',
    'Royals': 'KC',
    'Angels': 'LAA',
    'Dodgers': 'LAD',
    'Marlins': 'MIA',
    'Brewers': 'MIL',
    'Twins': 'MIN',
    'Mets': 'NYM',
    'Yankees': 'NYY',
    'Athletics': 'OAK',
    'Phillies': 'PHI',
    'Pirates': 'PIT',
    'Padres': 'SD',
    'Giants': 'SF',
    'Mariners': 'SEA',
    'Cardinals': 'STL',
    'Rays': 'TB',
    'Rangers': 'TEX',
    'Blue Jays': 'TOR',
    'Nationals': 'WAS'
}
"""A dict of MLB team abbreviations with full team name as key and abbreviation as key."""


fnames = [
    'yo',
    'ATC',
    'Depth_Charts',
    'Streamer',
    'THE_BAT',
    'ZiPS',
    'razzball'
]
"""A list of filenames."""


player_stats = {
    'hitter': ['G', 'PA', 'AB', 'H', '2B', '3B', 'HR', 'R', 'RBI', 'BB', 'SO', 'HBP', 'SB', 'CS'],
    'pitcher': ['G', 'GS', 'QS', 'IP', 'SV', 'HLD', 'H', 'ER', 'HR', 'SO', 'BB']
}
"""Counting stats of interest for both hitters and pitchers."""
