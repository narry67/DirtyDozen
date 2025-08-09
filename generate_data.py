import os
import json
from datetime import datetime
from espn_api.football import League

# ESPN API credentials
SWID = '{4812DD43-4CD8-4AFA-961D-8EE1D525B297}'
ESPN_S2 = 'AEA7oVs9WJDy9XucKDVRpt1nCt%2BbApmpPvQt6GPEmTHmok0LTw%2F3uyOKTsu14wND3%2Bozv%2BnNM40lWirXVd5EAjnDu0ZuDOjgeiaLQzKYC2OF6Fj37KSSPvkC1L8Y27tYnAkGfzYAbhH1dHFJz2JuoYhVTVar%2BoVlJRLKABUpqL5zUnf7WvzmuoIKJqogmyPXsVXeDa7oaaXKDB95zihG5PVKHm%2BblTyv8%2Bfo%2F%2BMzVRN3WGlP%2F5AgWZCjHN82ucEuAIr0CMUvxDMmsVgRN%2FYFMlApiE9KLqYq7boZVJ1f43VCNA%3D%3D'
LEAGUE_ID = 286725

def fetch_league_data():
    """Fetch comprehensive league data from ESPN API"""
    data = {}
    
    # Fetch data for multiple years (2014-2025)
    for year in range(2014, 2026):
        try:
            league = League(LEAGUE_ID, year, espn_s2=ESPN_S2, swid=SWID)
            
            year_data = {
                'teams': [],
                'standings': [],
                'draft': [],
                'settings': {},
                'box_scores': {},
                'power_rankings': [],
                'free_agents': [],
                'recent_activity': [],
                'league_stats': {}
            }
            
            # Team and standings data
            for team in league.teams:
                team_data = {
                    'team_id': getattr(team, 'team_id', None),
                    'team_name': getattr(team, 'team_name', ''),
                    'team_abbrev': getattr(team, 'team_abbrev', ''),
                    'division_name': getattr(team, 'division_name', ''),
                    'wins': getattr(team, 'wins', 0),
                    'losses': getattr(team, 'losses', 0),
                    'ties': getattr(team, 'ties', 0),
                    'points_for': float(getattr(team, 'points_for', 0) or 0),
                    'points_against': float(getattr(team, 'points_against', 0) or 0),
                    'waiver_rank': getattr(team, 'waiver_rank', None),
                    'acquisitions': getattr(team, 'acquisitions', 0),
                    'acquisition_budget_spent': getattr(team, 'acquisition_budget_spent', 0),
                    'drops': getattr(team, 'drops', 0),
                    'trades': getattr(team, 'trades', 0),
                    'move_to_ir': getattr(team, 'move_to_ir', 0),
                    'streak_type': getattr(team, 'streak_type', ''),
                    'streak_length': getattr(team, 'streak_length', 0),
                    'standing': getattr(team, 'standing', None),
                    'final_standing': getattr(team, 'final_standing', None),
                    'draft_projected_rank': getattr(team, 'draft_projected_rank', None),
                    'playoff_pct': getattr(team, 'playoff_pct', None),
                    'logo_url': getattr(team, 'logo_url', ''),
                    'roster': []
                }
                
                # Player roster data
                for player in team.roster:
                    player_data = {
                        'name': getattr(player, 'name', ''),
                        'playerId': getattr(player, 'playerId', None),
                        'position': getattr(player, 'position', ''),
                        'posRank': getattr(player, 'posRank', None),
                        'proTeam': getattr(player, 'proTeam', ''),
                        'eligibleSlots': getattr(player, 'eligibleSlots', []) or [],
                        'lineupSlot': getattr(player, 'lineupSlot', ''),
                        'acquisitionType': getattr(player, 'acquisitionType', ''),
                        'injuryStatus': getattr(player, 'injuryStatus', ''),
                        'injured': getattr(player, 'injured', False),
                        'total_points': float(getattr(player, 'total_points', 0) or 0),
                        'avg_points': float(getattr(player, 'avg_points', 0) or 0),
                        'projected_total_points': float(getattr(player, 'projected_total_points', 0) or 0),
                        'projected_avg_points': float(getattr(player, 'projected_avg_points', 0) or 0),
                        'percent_owned': getattr(player, 'percent_owned', None),
                        'percent_started': getattr(player, 'percent_started', None)
                    }
                    team_data['roster'].append(player_data)
                
                year_data['teams'].append(team_data)
                year_data['standings'].append({
                    'team_name': team.team_name,
                    'wins': team.wins,
                    'losses': team.losses,
                    'points_for': team.points_for,
                    'points_against': team.points_against
                })
            
            # League settings
            settings = league.settings
            year_data['settings'] = {
                'name': getattr(settings, 'name', ''),
                'team_count': getattr(settings, 'team_count', 0),
                'reg_season_count': getattr(settings, 'reg_season_count', 13),
                'playoff_team_count': getattr(settings, 'playoff_team_count', None),
                'keeper_count': getattr(settings, 'keeper_count', 0),
                'veto_votes_required': getattr(settings, 'veto_votes_required', None),
                'trade_deadline': getattr(settings, 'trade_deadline', None),
                'tie_rule': getattr(settings, 'tie_rule', None),
                'playoff_tie_rule': getattr(settings, 'playoff_tie_rule', None),
                'playoff_seed_tie_rule': getattr(settings, 'playoff_seed_tie_rule', None),
                'playoff_matchup_period_length': getattr(settings, 'playoff_matchup_period_length', None),
                'faab': getattr(settings, 'faab', False),
                'acquisition_budget': getattr(settings, 'acquisition_budget', None),
                'scoring_format': getattr(settings, 'scoring_format', [])
            }
            
            # Draft information
            for pick in league.draft:
                pick_data = {
                    'playerId': pick.playerId,
                    'playerName': pick.playerName,
                    'round_num': pick.round_num,
                    'round_pick': pick.round_pick,
                    'bid_amount': pick.bid_amount,
                    'keeper_status': pick.keeper_status,
                    'team_name': pick.team.team_name if pick.team else None,
                    'nominating_team': pick.nominatingTeam.team_name if pick.nominatingTeam else None
                }
                year_data['draft'].append(pick_data)
            
            # Weekly scores (box scores for 2018+, scoreboard for earlier years)
            try:
                weeks_in_season = int(year_data['settings'].get('reg_season_count') or 13)
                for week in range(1, weeks_in_season + 1):
                    try:
                        week_scores = []
                        if year >= 2018:
                            box_scores = league.box_scores(week)
                            for box_score in box_scores:
                                score_data = {
                                    'home_team': getattr(box_score.home_team, 'team_name', ''),
                                    'away_team': getattr(box_score.away_team, 'team_name', ''),
                                    'home_score': float(getattr(box_score, 'home_score', 0) or 0),
                                    'away_score': float(getattr(box_score, 'away_score', 0) or 0),
                                    'home_projected': getattr(box_score, 'home_projected', None),
                                    'away_projected': getattr(box_score, 'away_projected', None),
                                    'is_playoff': getattr(box_score, 'is_playoff', False),
                                    'matchup_type': getattr(box_score, 'matchup_type', 'NONE'),
                                    'home_lineup': [],
                                    'away_lineup': []
                                }
                                for player in getattr(box_score, 'home_lineup', []) or []:
                                    score_data['home_lineup'].append({
                                        'name': getattr(player, 'name', ''),
                                        'position': getattr(player, 'position', ''),
                                        'slot_position': getattr(player, 'slot_position', ''),
                                        'points': float(getattr(player, 'points', 0) or 0),
                                        'projected_points': float(getattr(player, 'projected_points', 0) or 0),
                                        'pro_opponent': getattr(player, 'pro_opponent', ''),
                                        'pro_pos_rank': getattr(player, 'pro_pos_rank', None),
                                        'game_played': getattr(player, 'game_played', 0),
                                        'game_date': str(getattr(player, 'game_date', '') or '') if getattr(player, 'game_date', None) else None,
                                        'on_bye_week': getattr(player, 'on_bye_week', False),
                                        'active_status': getattr(player, 'active_status', '')
                                    })
                                for player in getattr(box_score, 'away_lineup', []) or []:
                                    score_data['away_lineup'].append({
                                        'name': getattr(player, 'name', ''),
                                        'position': getattr(player, 'position', ''),
                                        'slot_position': getattr(player, 'slot_position', ''),
                                        'points': float(getattr(player, 'points', 0) or 0),
                                        'projected_points': float(getattr(player, 'projected_points', 0) or 0),
                                        'pro_opponent': getattr(player, 'pro_opponent', ''),
                                        'pro_pos_rank': getattr(player, 'pro_pos_rank', None),
                                        'game_played': getattr(player, 'game_played', 0),
                                        'game_date': str(getattr(player, 'game_date', '') or '') if getattr(player, 'game_date', None) else None,
                                        'on_bye_week': getattr(player, 'on_bye_week', False),
                                        'active_status': getattr(player, 'active_status', '')
                                    })
                                week_scores.append(score_data)
                        else:
                            # Use scoreboard for seasons before 2018
                            matchups = league.scoreboard(week)
                            for m in matchups:
                                week_scores.append({
                                    'home_team': getattr(m.home_team, 'team_name', ''),
                                    'away_team': getattr(m.away_team, 'team_name', ''),
                                    'home_score': float(getattr(m, 'home_score', 0) or 0),
                                    'away_score': float(getattr(m, 'away_score', 0) or 0),
                                    'home_projected': None,
                                    'away_projected': None,
                                    'is_playoff': False,
                                    'matchup_type': 'NONE',
                                    'home_lineup': [],
                                    'away_lineup': []
                                })
                        if week_scores:
                            year_data['box_scores'][str(week)] = week_scores
                    except Exception as e:
                        print(f"Error fetching box scores for week {week} in {year}: {e}")
                        continue
            except Exception as e:
                print(f"Error fetching box scores for {year}: {e}")
            
            # Power rankings
            try:
                power_rankings = league.power_rankings()
                for score, team in power_rankings:
                    year_data['power_rankings'].append({
                        'score': score,
                        'team_name': team.team_name
                    })
            except Exception as e:
                print(f"Error fetching power rankings for {year}: {e}")
            
            # Free agents (current season only)
            if year == datetime.now().year:
                try:
                    free_agents = league.free_agents(size=50)
                    for player in free_agents:
                        fa_data = {
                            'name': player.name,
                            'position': player.position,
                            'proTeam': player.proTeam,
                            'percent_owned': player.percent_owned,
                            'total_points': player.total_points,
                            'avg_points': player.avg_points
                        }
                        year_data['free_agents'].append(fa_data)
                except Exception as e:
                    print(f"Error fetching free agents for {year}: {e}")
            
            # Recent activity (2019+ only and current season). Fetch FA, WAIVER, TRADED separately
            if year == datetime.now().year and year >= 2019:
                try:
                    combined = []
                    for msg in ['FA', 'WAIVER', 'TRADED']:
                        try:
                            acts = league.recent_activity(size=50, msg_type=msg)
                            combined.extend(acts)
                        except Exception as inner_e:
                            # Some message types may not be available; skip
                            continue
                    for activity in combined:
                        activity_data = {
                            'date': getattr(activity, 'date', None),
                            'actions': []
                        }
                        for item in getattr(activity, 'actions', []) or []:
                            # Each item is expected as (Team, action, Player, [bid_amount])
                            team = item[0] if len(item) > 0 else None
                            action = item[1] if len(item) > 1 else ''
                            player = item[2] if len(item) > 2 else ''
                            bid_amount = item[3] if len(item) > 3 else None
                            activity_data['actions'].append({
                                'team_name': getattr(team, 'team_name', None) if team else None,
                                'action': action,
                                'player': getattr(player, 'name', str(player)) if player is not None else '',
                                'bid_amount': bid_amount
                            })
                        year_data['recent_activity'].append(activity_data)
                except Exception as e:
                    print(f"Error fetching recent activity for {year}: {e}")
            
            # League statistics
            try:
                year_data['league_stats'] = {
                    'top_scorer': league.top_scorer().team_name if league.top_scorer() else None,
                    'least_scorer': league.least_scorer().team_name if league.least_scorer() else None,
                    'most_points_against': league.most_points_against().team_name if league.most_points_against() else None,
                    'top_scored_week': {
                        'team': league.top_scored_week()[0].team_name if league.top_scored_week() else None,
                        'points': league.top_scored_week()[1] if league.top_scored_week() else None
                    },
                    'least_scored_week': {
                        'team': league.least_scored_week()[0].team_name if league.least_scored_week() else None,
                        'points': league.least_scored_week()[1] if league.least_scored_week() else None
                    }
                }
            except Exception as e:
                print(f"Error fetching league stats for {year}: {e}")
            
            data[str(year)] = year_data
            print(f"✅ Successfully fetched data for {year}")
            
        except Exception as e:
            print(f"❌ Error fetching data for {year}: {e}")
            continue
    
    return data

def generate_html_template(data):
    data_json = json.dumps(data)

    # Generate year buttons
    year_buttons = ""
    for year in sorted(data.keys(), reverse=True):
        year_buttons += f'<button class="year-btn" onclick="showYear({year})">{year}</button>'

    # Generate year content
    year_content = ""
    for year, year_data in data.items():
        # Generate standings rows
        standings_rows = ""
        for team in year_data['standings']:
            standings_rows += f"""
                <tr>
                    <td>{team['team_name']}</td>
                    <td>{team['wins']}</td>
                    <td>{team['losses']}</td>
                    <td>{team['points_for']:.2f}</td>
                    <td>{team['points_against']:.2f}</td>
                </tr>"""

        # Generate team rosters
        team_rosters = ""
        for team in year_data['teams']:
            team_rosters += f"""
                <div class="team-section">
                    <h4>{team['team_name']} ({team['wins']}-{team['losses']})</h4>
                    <div class="team-stats">
                        <span>Points For: {team['points_for']:.2f}</span>
                        <span>Points Against: {team['points_against']:.2f}</span>
                        <span>Streak: {team['streak_type']} {team['streak_length']}</span>
                        <span>Acquisitions: {team['acquisitions']}</span>
                        <span>Trades: {team['trades']}</span>
                    </div>
                    <table class="roster-table">
                        <tr>
                            <th>Player</th>
                            <th>Position</th>
                            <th>Pro Team</th>
                            <th>Total Points</th>
                            <th>Avg Points</th>
                        </tr>"""
            
            for player in team['roster']:
                team_rosters += f"""
                        <tr>
                            <td>{player['name']}</td>
                            <td>{player['position']}</td>
                            <td>{player['proTeam']}</td>
                            <td>{player['total_points']:.2f}</td>
                            <td>{player['avg_points']:.2f}</td>
                        </tr>"""
            
            team_rosters += """
                    </table>
                </div>"""

        # Generate trade history
        trade_history = ""
        for activity in year_data['recent_activity']:
            for action in activity['actions']:
                if action['action'] == 'TRADED':
                    trade_history += f"""
                        <div class="trade-item">
                            <span class="trade-date">{datetime.fromtimestamp(activity['date']/1000).strftime('%Y-%m-%d %H:%M')}</span>
                            <span class="trade-team">{action['team_name']}</span>
                            <span class="trade-action">{action['action']}</span>
                            <span class="trade-player">{action['player']}</span>
                        </div>"""

        # Generate power rankings rows
        power_rankings_rows = ""
        for i, ranking in enumerate(year_data['power_rankings'], 1):
            power_rankings_rows += f"""
                <tr>
                    <td>{i}</td>
                    <td>{ranking['team_name']}</td>
                    <td>{ranking['score']}</td>
                </tr>"""

        # Generate statistics cards
        stats = year_data['league_stats']
        statistics_cards = f"""
            <div class="stats-grid">
                <div class="stat-card">
                    <h4>Top Scorer</h4>
                    <p>{stats.get('top_scorer', 'N/A')}</p>
                </div>
                <div class="stat-card">
                    <h4>Least Scorer</h4>
                    <p>{stats.get('least_scorer', 'N/A')}</p>
                </div>
                <div class="stat-card">
                    <h4>Most Points Against</h4>
                    <p>{stats.get('most_points_against', 'N/A')}</p>
                </div>
                <div class="stat-card">
                    <h4>Highest Week Score</h4>
                    <p>{stats.get('top_scored_week', {}).get('team', 'N/A')} - {stats.get('top_scored_week', {}).get('points', 'N/A')}</p>
                </div>
                <div class="stat-card">
                    <h4>Lowest Week Score</h4>
                    <p>{stats.get('least_scored_week', {}).get('team', 'N/A')} - {stats.get('least_scored_week', {}).get('points', 'N/A')}</p>
                </div>
            </div>"""

        # Generate draft information (aligned table)
        draft_info_rows = ""
        for pick in year_data['draft']:
            draft_info_rows += f"""
                <tr>
                    <td>{pick['round_num']}.{pick['round_pick']}</td>
                    <td>{pick['team_name'] or ''}</td>
                    <td>{pick['playerName']}</td>
                    <td class="num">{pick['bid_amount'] if pick['bid_amount'] else ''}</td>
                </tr>"""
        draft_info = f"""
            <table class=\"draft-table\">
                <tr>
                    <th>Round.Pick</th>
                    <th>Team</th>
                    <th>Player</th>
                    <th class=\"num\">Bid</th>
                </tr>
                {draft_info_rows}
            </table>"""

        # Generate box scores (aligned with scores close to team names)
        box_scores_content = ""
        for week, scores in year_data['box_scores'].items():
            rows = ""
            for score in scores:
                rows += f"""
                    <tr>
                        <td class=\"team-cell\"><div class=\"team-flex\"><span class=\"team-name\">{score['home_team']}</span><span class=\"score-chip\">{score['home_score']:.2f}</span></div></td>
                        <td class=\"vs-cell\">vs</td>
                        <td class=\"team-cell\"><div class=\"team-flex\"><span class=\"team-name\">{score['away_team']}</span><span class=\"score-chip\">{score['away_score']:.2f}</span></div></td>
                    </tr>"""
            box_scores_content += f"""
                <div class=\"week-section\">
                    <h4>Week {week}</h4>
                    <table class=\"box-table\">
                        <tr>
                            <th class=\"team-col\">Home</th>
                            <th class=\"vs-col\"></th>
                            <th class=\"team-col\">Away</th>
                        </tr>
                        {rows}
                    </table>
                </div>"""

        # Generate settings information
        settings = year_data['settings']
        settings_info = f"""
            <div class="settings-grid">
                <div class="setting-item">
                    <h4>League Name</h4>
                    <p>{settings['name']}</p>
                </div>
                <div class="setting-item">
                    <h4>Teams</h4>
                    <p>{settings['team_count']}</p>
                </div>
                <div class="setting-item">
                    <h4>Regular Season</h4>
                    <p>{settings['reg_season_count']} weeks</p>
                </div>
                <div class="setting-item">
                    <h4>Playoff Teams</h4>
                    <p>{settings['playoff_team_count']}</p>
                </div>
                <div class="setting-item">
                    <h4>Trade Deadline</h4>
                    <p>{datetime.fromtimestamp(settings['trade_deadline']/1000).strftime('%Y-%m-%d') if settings['trade_deadline'] else 'N/A'}</p>
                </div>
                <div class="setting-item">
                    <h4>Veto Votes Required</h4>
                    <p>{settings['veto_votes_required']}</p>
                </div>
            </div>"""

        year_content += f"""
            <div id="year-{year}" class="year-content" style="display: none;">
                <h2>{year} Season</h2>
                <div class="tab-container">
                    <button class="tab-button active" onclick="showTab('standings-{year}')">Standings</button>
                    <button class="tab-button" onclick="showTab('teams-{year}')">Teams</button>
                    <button class="tab-button" onclick="showTab('activity-{year}')">Trade History</button>
                    <button class="tab-button" onclick="showTab('stats-{year}')">Statistics</button>
                    <button class="tab-button" onclick="showTab('draft-{year}')">Draft</button>
                    <button class="tab-button" onclick="showTab('boxscores-{year}')">Box Scores</button>
                    <button class="tab-button" onclick="showTab('power-{year}')">Power Rankings</button>
                    <button class="tab-button" onclick="showTab('settings-{year}')">Settings</button>
                </div>
                
                <div id="standings-{year}" class="tab-content card active">
                    <h3>League Standings</h3>
                    <div class="chart-container">
                        <canvas id="standings-chart-{year}"></canvas>
                    </div>
                    <table>
                        <tr>
                            <th>Team</th>
                            <th>Wins</th>
                            <th>Losses</th>
                            <th>Points For</th>
                            <th>Points Against</th>
                        </tr>
                        {standings_rows}
                    </table>
                </div>
                
                <div id="teams-{year}" class="tab-content card">
                    <h3>Team Rosters</h3>
                    {team_rosters}
                </div>
                
                <div id="activity-{year}" class="tab-content card">
                    <h3>Recent Activity</h3>
                    <div class="activity-list">
                        {trade_history}
                    </div>
                </div>
                
                <div id="stats-{year}" class="tab-content card">
                    <h3>League Statistics</h3>
                    {statistics_cards}
                </div>
                
                <div id="draft-{year}" class="tab-content card">
                    <h3>Draft Results</h3>
                    <div class="draft-list">
                        {draft_info}
                    </div>
                </div>
                
                <div id="boxscores-{year}" class="tab-content card">
                    <h3>Weekly Box Scores</h3>
                    <div class="box-scores">
                        {box_scores_content}
                    </div>
                </div>
                
                <div id="power-{year}" class="tab-content card">
                    <h3>Power Rankings</h3>
                    <div class="chart-container">
                        <canvas id="power-chart-{year}"></canvas>
                    </div>
                    <table>
                        <tr>
                            <th>Rank</th>
                            <th>Team</th>
                            <th>Score</th>
                        </tr>
                        {''.join([f"<tr><td>{i+1}</td><td>{pr['team_name']}</td><td class='num'>{pr['score']}</td></tr>" for i, pr in enumerate(year_data['power_rankings'])])}
                    </table>
                </div>

                <div id="settings-{year}" class="tab-content card">
                    <h3>League Settings</h3>
                    {settings_info}
                </div>
            </div>"""

    return f'''<!DOCTYPE html>
<html>
<head>
    <title>😈 The Dirty Dozen 😈</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.7.0/chart.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1f2937 100%);
            min-height: 100vh;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        h1 {{
            text-align: center;
            color: white;
            margin-bottom: 10px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .last-updated {{
            text-align: center;
            color: rgba(255,255,255,0.8);
            margin-bottom: 30px;
            font-style: italic;
        }}
        
        .year-selector {{
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .year-btn {{
            background: rgba(255,255,255,0.2);
            border: 2px solid rgba(255,255,255,0.3);
            color: white;
            padding: 10px 20px;
            margin: 0 5px;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
        }}
        
        .year-btn:hover {{
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }}
        
        .year-btn.active {{
            background: rgba(255,255,255,0.4);
            border-color: white;
        }}
        
        .year-content {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-top: 20px;
        }}
        
        .tab-container {{
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .tab-button {{
            background: #f8f9fa;
            border: 2px solid #dee2e6;
            color: #495057;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }}
        
        .tab-button:hover {{
            background: #e9ecef;
            transform: translateY(-1px);
        }}
        
        .tab-button.active {{
            background: #2563eb;
            color: white;
            border-color: #2563eb;
        }}
        
        .tab-content {{
            display: none;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .card {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        h3 {{
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 3px solid #2563eb;
            padding-bottom: 10px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        th, td {{
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }}
        
        th {{
            background: #1f2937;
            color: white;
            font-weight: 600;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        .chart-container {{
            height: 400px;
            margin: 20px 0;
        }}
        
        .team-section {{
            margin-bottom: 30px;
            padding: 20px;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            background: #f8f9fa;
        }}
        
        .team-section h4 {{
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}
        
        .team-stats {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 15px;
        }}
        
        .team-stats span {{
            background: #2563eb;
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.9em;
        }}
        
        .roster-table {{
            font-size: 0.9em;
        }}
        
        .activity-list {{
            max-height: 400px;
            overflow-y: auto;
        }}
        
        .trade-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px;
            border-bottom: 1px solid #dee2e6;
            background: #f8f9fa;
            margin-bottom: 5px;
            border-radius: 5px;
        }}
        
        .trade-date {{
            color: #6c757d;
            font-size: 0.9em;
        }}
        
        .trade-team {{
            font-weight: bold;
            color: #007bff;
        }}
        
        .trade-action {{
            color: #28a745;
            font-weight: bold;
        }}
        
        .trade-player {{
            color: #495057;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #1f2937 0%, #2563eb 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        .stat-card h4 {{
            margin-bottom: 10px;
            font-size: 1.1em;
        }}
        
        .stat-card p {{
            font-size: 1.2em;
            font-weight: bold;
        }}
        
        .draft-list {{
            max-height: 400px;
            overflow-y: auto;
        }}
        
        .draft-table, .box-table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}
        .draft-table th, .draft-table td, .box-table th, .box-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid #e9ecef;
        }}
        .draft-table th, .box-table th {{
            background: #f1f3f5;
            color: #343a40;
            font-weight: 600;
        }}
        .num {{
            text-align: right;
            font-variant-numeric: tabular-nums;
        }}

        /* Box score alignment helpers */
        .team-col {{ width: 45%; }}
        .vs-col {{ width: 10%; text-align: center; color: #6c757d; }}
        .team-cell {{ padding: 8px 12px; }}
        .team-flex {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
        }}
        .team-name {{
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            max-width: 75%;
        }}
        .score-chip {{
            background: #0ea5e9;
            color: #0b1324;
            border: 1px solid #0891b2;
            padding: 2px 8px;
            border-radius: 999px;
            font-weight: 600;
            font-variant-numeric: tabular-nums;
            min-width: 56px;
            text-align: right;
        }}
        
        .box-scores {{
            max-height: 500px;
            overflow-y: auto;
        }}
        
        .week-section {{
            margin-bottom: 20px;
            padding: 15px;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            background: #f8f9fa;
        }}
        
        .week-section h4 {{
            color: #2c3e50;
            margin-bottom: 15px;
        }}
        
        /* removed old flex matchup styles in favor of tables */
        
        .settings-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .setting-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border: 2px solid #e9ecef;
        }}
        
        .setting-item h4 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 1em;
        }}
        
        .setting-item p {{
            color: #495057;
            font-weight: bold;
            font-size: 1.1em;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            
            .tab-container {{
                flex-direction: column;
                align-items: center;
            }}
            
            .team-stats {{
                flex-direction: column;
            }}
            
            .trade-item, .draft-pick, .matchup {{
                flex-direction: column;
                text-align: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>😈 The Dirty Dozen 😈</h1>
        <div class="last-updated">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>

        <div class="year-selector">
            {year_buttons}
        </div>

        {year_content}
    </div>

    <script>
        const data = {data_json};
        
        function showYear(year) {{
            // Hide all year content
            document.querySelectorAll('.year-content').forEach(content => {{
                content.style.display = 'none';
            }});
            
            // Show selected year content
            document.getElementById(`year-${{year}}`).style.display = 'block';
            
            // Update year button styles
            document.querySelectorAll('.year-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            if (typeof event !== 'undefined' && event && event.target) {{
                event.target.classList.add('active');
            }} else {{
                const btn = Array.from(document.querySelectorAll('.year-btn')).find(b => b.getAttribute('onclick') === `showYear(${{year}})`);
                if (btn) btn.classList.add('active');
            }}
            
            // Initialize charts for the selected year
            initializeCharts(year);
        }}
        
        function showTab(tabId) {{
            const year = tabId.split('-')[1];
            const tabContent = document.getElementById(tabId);
            
            // Hide all tab content for this year
            document.querySelectorAll(`#year-${{year}} .tab-content`).forEach(content => {{
                content.classList.remove('active');
            }});
            
            // Show selected tab content
            tabContent.classList.add('active');
            
            // Update tab button styles
            document.querySelectorAll(`#year-${{year}} .tab-button`).forEach(btn => {{
                btn.classList.remove('active');
            }});
            if (typeof event !== 'undefined' && event && event.target) {{
                event.target.classList.add('active');
            }}
        }}
        
        function initializeCharts(year) {{
            const yearData = data[year];
            if (!yearData) return;
            
            // Create standings chart
            const ctx = document.getElementById(`standings-chart-${{year}}`);
            if (ctx) {{
                const standings = yearData.standings;
                const labels = standings.map(team => team.team_name);
                const pointsFor = standings.map(team => team.points_for);
                const pointsAgainst = standings.map(team => team.points_against);
                
                new Chart(ctx, {{
                    type: 'bar',
                    data: {{
                        labels: labels,
                        datasets: [
                            {{
                                label: 'Points For',
                                data: pointsFor,
                                backgroundColor: 'rgba(37, 99, 235, 0.8)',
                                borderColor: 'rgba(37, 99, 235, 1)',
                                borderWidth: 1
                            }},
                             {{
                                label: 'Points Against',
                                data: pointsAgainst,
                                backgroundColor: 'rgba(0, 0, 0, 0.85)',
                                borderColor: 'rgba(0, 0, 0, 1)',
                                borderWidth: 1
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
                                beginAtZero: true
                            }}
                        }},
                        plugins: {{
                            title: {{
                                display: true,
                                text: 'Team Performance Comparison'
                            }}
                        }}
                    }}
                }});
            }}

            // Create power rankings chart (bar)
            const pctx = document.getElementById(`power-chart-${{year}}`);
            if (pctx && yearData.power_rankings && yearData.power_rankings.length) {{
                const labels = yearData.power_rankings.map(pr => pr.team_name);
                const scores = yearData.power_rankings.map(pr => Number(pr.score));
                new Chart(pctx, {{
                    type: 'bar',
                    data: {{
                        labels: labels,
                        datasets: [{{
                            label: 'Power Score',
                            data: scores,
                            backgroundColor: 'rgba(37, 99, 235, 0.8)',
                            borderColor: 'rgba(37, 99, 235, 1)',
                            borderWidth: 1
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{ y: {{ beginAtZero: true }} }},
                        plugins: {{ title: {{ display: true, text: 'Power Rankings' }} }}
                    }}
                }});
            }}
        }}
        
        // Initialize the first year on page load
        document.addEventListener('DOMContentLoaded', function() {{
            const firstYear = Object.keys(data).sort((a, b) => b - a)[0];
            if (firstYear) {{
                showYear(firstYear);
            }}
        }});
    </script>
</body>
</html>'''

def generate_html():
    """Generate the complete HTML dashboard"""
    print("🔄 Fetching league data from ESPN API...")
    data = fetch_league_data()
    
    if not data:
        print("❌ No data retrieved. Please check your ESPN API credentials.")
        return
    
    print("📊 Generating HTML dashboard...")
    html_content = generate_html_template(data)
    
    # Ensure docs directory exists
    os.makedirs('docs', exist_ok=True)
    
    # Write HTML file
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Dashboard generated successfully!")
    print(f"📁 File saved to: docs/index.html")
    print(f"📊 Data includes {len(data)} seasons")
    
    # Print summary
    for year, year_data in data.items():
        print(f"   {year}: {len(year_data['teams'])} teams, {len(year_data['draft'])} draft picks")

if __name__ == "__main__":
    generate_html() 