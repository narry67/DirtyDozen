#!/usr/bin/env python3
"""
Test script to verify the data generation works locally.
Run this before pushing to GitHub to ensure everything works.
"""

import os
import sys
from generate_data import generate_html

def test_generation():
    """Test the HTML generation process"""
    try:
        print("Testing HTML generation...")
        generate_html()
        
        # Check if the file was created
        if os.path.exists('docs/index.html'):
            file_size = os.path.getsize('docs/index.html')
            print(f"✅ Success! Generated docs/index.html ({file_size} bytes)")
            
            # Check if the file has content
            with open('docs/index.html', 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content) > 1000:  # Basic size check
                    print("✅ HTML file has substantial content")
                else:
                    print("⚠️  HTML file seems small, may indicate an issue")
                    
        else:
            print("❌ Failed to generate docs/index.html")
            return False
            
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = test_generation()
    sys.exit(0 if success else 1) 