# Fantasy Football League Dashboard

A static dashboard that displays fantasy football league statistics and data from ESPN's API. The dashboard is automatically updated weekly via GitHub Actions and hosted on GitHub Pages.

## Features

- **League Standings**: Current standings with wins, losses, points for/against
- **Power Rankings**: Custom power ranking algorithm based on points scored, winning percentage, and median performance
- **Team Rosters**: Detailed player information for each team
- **Trade History**: Recent trade activity in the league
- **Season Statistics**: Top/least scorers, highest/lowest scoring weeks, most points against
- **Interactive Charts**: Visual representations of standings and power rankings
- **Multi-Year Support**: View data from 2014 to present

## Setup Instructions

### 1. Repository Setup

1. **Fork or clone this repository**
2. **Enable GitHub Pages**:
   - Go to your repository Settings
   - Navigate to "Pages" in the sidebar
   - Under "Source", select "Deploy from a branch"
   - Choose "gh-pages" branch
   - Click "Save"

### 2. Configure ESPN API Credentials

The dashboard uses ESPN's API to fetch league data. You'll need to update the credentials in `generate_data.py`:

```python
# ESPN API credentials
SWID = "your-swid-here"
ESPN_S2 = "your-espn-s2-here"
LEAGUE_ID = your-league-id
```

**How to get these credentials:**
1. Log into ESPN Fantasy Football
2. Open browser developer tools (F12)
3. Go to Application/Storage tab
4. Look for cookies named `SWID` and `espn_s2`
5. Copy their values
6. Find your league ID in the URL when viewing your league

### 3. Enable GitHub Actions

1. Go to your repository Settings
2. Navigate to "Actions" → "General"
3. Ensure "Actions permissions" is set to "Allow all actions and reusable workflows"
4. Save the changes

### 4. Initial Deployment

1. **Commit and push your changes**:
   ```bash
   git add .
   git commit -m "Initial setup"
   git push origin main
   ```

2. **Trigger the workflow manually**:
   - Go to the "Actions" tab in your repository
   - Click on "Update Fantasy Football Dashboard"
   - Click "Run workflow" → "Run workflow"

### 5. Verify Deployment

After the workflow completes:
1. Go to your repository Settings → Pages
2. You should see a green checkmark indicating successful deployment
3. Click the provided URL to view your dashboard

## How It Works

### Static Generation
- The `generate_data.py` script fetches data from ESPN's API
- It generates a complete static HTML file with embedded data
- The HTML file is placed in the `docs/` directory

### Automated Updates
- GitHub Actions runs every Sunday at 2 AM UTC
- It installs dependencies, runs the data generation script
- Deploys the updated dashboard to GitHub Pages

### Manual Updates
You can manually trigger updates by:
1. Going to the "Actions" tab
2. Selecting "Update Fantasy Football Dashboard"
3. Clicking "Run workflow"

## File Structure

```
├── .github/workflows/
│   └── update-dashboard.yml    # GitHub Actions workflow
├── docs/
│   └── index.html              # Generated static site
├── generate_data.py            # Data generation script
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## Troubleshooting

### Common Issues

1. **Power Rankings or Trade History showing blank**:
   - This is a known issue with the ESPN API
   - The dashboard will still work for other features
   - Check the ESPN API documentation for updates

2. **GitHub Actions failing**:
   - Check the Actions tab for error details
   - Ensure your ESPN credentials are correct
   - Verify the league ID is valid

3. **Dashboard not updating**:
   - Check if the workflow is running on schedule
   - Verify the gh-pages branch is being updated
   - Ensure GitHub Pages is configured correctly

### Security Notes

- **Never commit your ESPN credentials** to the repository
- Consider using GitHub Secrets for sensitive data
- The current setup has credentials hardcoded for simplicity

## Customization

### Adding New Features
1. Modify `generate_data.py` to fetch additional data
2. Update the HTML template in the `generate_html_template()` function
3. Add corresponding JavaScript for interactivity

### Changing Update Schedule
Edit the cron expression in `.github/workflows/update-dashboard.yml`:
```yaml
schedule:
  - cron: '0 2 * * 0'  # Every Sunday at 2 AM UTC
```

### Styling
The dashboard uses embedded CSS. To modify the appearance, edit the `<style>` section in the `generate_html_template()` function.

## Support

If you encounter issues:
1. Check the GitHub Actions logs for error messages
2. Verify your ESPN credentials are correct
3. Ensure your league is accessible via the ESPN API
4. Check that GitHub Pages is properly configured

## License

This project is open source and available under the MIT License. 