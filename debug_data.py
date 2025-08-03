#!/usr/bin/env python3
"""
Debug script to check what data is being retrieved from ESPN API
"""

from generate_data import get_all_years_data, datetime

def debug_data():
    print("Fetching data from ESPN API...")
    leagues_data = get_all_years_data()
    
    print(f"\nFound data for years: {list(leagues_data.keys())}")
    
    for year, league in leagues_data.items():
        print(f"\n=== {year} Season ===")
        
        try:
            # Check standings
            standings = league.standings()
            print(f"Standings: {len(standings)} teams found")
            for team in standings[:3]:  # Show first 3 teams
                print(f"  - {team.team_name}: {team.wins}-{team.losses}, {team.points_for:.1f} pts")
            
            # Check teams
            print(f"Teams: {len(league.teams)} teams found")
            
            # Check if current year has power rankings
            if year == datetime.now().year:
                try:
                    from generate_data import calculate_custom_power_rankings
                    power_rankings = calculate_custom_power_rankings(league)
                    print(f"Power Rankings: {len(power_rankings)} teams ranked")
                except Exception as e:
                    print(f"Power Rankings: Error - {e}")
            
            # Check recent activity
            try:
                activity = league.recent_activity(msg_type='TRADED')
                print(f"Recent Activity: {len(activity)} trades found")
            except Exception as e:
                print(f"Recent Activity: Error - {e}")
                
        except Exception as e:
            print(f"Error processing {year}: {e}")

if __name__ == '__main__':
    debug_data() 