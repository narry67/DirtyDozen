#!/usr/bin/env python3
"""
Test ESPN API with past years
"""

from espn_api.football import League
from generate_data import LEAGUE_ID, ESPN_S2, SWID

def test_past_years():
    print("Testing ESPN API with past years...")
    
    for year in [2023, 2022, 2021, 2020]:
        try:
            print(f"\nTrying {year}...")
            league = League(league_id=LEAGUE_ID, year=year, espn_s2=ESPN_S2, swid=SWID)
            
            # Try to get basic info
            standings = league.standings()
            print(f"✅ {year}: {len(standings)} teams found")
            
            # Show first team as example
            if standings:
                first_team = standings[0]
                print(f"   Example: {first_team.team_name} - {first_team.wins}-{first_team.losses}")
            
        except Exception as e:
            print(f"❌ {year}: {e}")

if __name__ == '__main__':
    test_past_years() 