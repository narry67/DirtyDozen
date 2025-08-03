#!/usr/bin/env python3
"""
Debug script to test ESPN API connection
"""

from espn_api.football import League
from generate_data import LEAGUE_ID, ESPN_S2, SWID

def test_connection():
    print("Testing ESPN API connection...")
    print(f"League ID: {LEAGUE_ID}")
    print(f"ESPN_S2: {ESPN_S2[:20]}...")
    print(f"SWID: {SWID[:20]}...")
    
    try:
        # Try to get current year data
        from datetime import datetime
        current_year = datetime.now().year
        print(f"\nTrying to fetch {current_year} season...")
        
        league = League(league_id=LEAGUE_ID, year=current_year, espn_s2=ESPN_S2, swid=SWID)
        print("✅ Successfully connected to ESPN API!")
        
        # Try to get basic info
        print(f"League name: {league.settings.name if hasattr(league, 'settings') else 'Unknown'}")
        print(f"Number of teams: {len(league.teams)}")
        
        # Try to get standings
        try:
            standings = league.standings()
            print(f"Standings available: {len(standings)} teams")
        except Exception as e:
            print(f"Standings error: {e}")
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nPossible issues:")
        print("1. Invalid League ID")
        print("2. Expired ESPN credentials")
        print("3. League is private or not accessible")
        print("4. Network connectivity issues")

if __name__ == '__main__':
    test_connection() 