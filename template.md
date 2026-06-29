# Project Title

Historical NHL Betting Simulator and Sports Analytics Platform

---

# Problem Statement

Sports betting research platforms often focus on live betting or proprietary data, making it difficult for users to evaluate historical betting strategies. There is a lack of interactive systems that allow users to replay historical NHL seasons, place simulated bets using historical bookmaker odds, and analyze betting performance over an entire season.

This project aims to provide a historical betting simulation environment that combines historical NHL match data with historical sportsbook odds to create an educational and analytical platform for sports betting research.

---

# Proposed Solution

Develop a historical NHL betting simulator that enables users to:

* Browse historical NHL fixtures.
* Place simulated bets using historical bookmaker odds.
* Track bankroll performance throughout a season.
* Review betting history and betting statistics.
* Serve as a foundation for future probability models, betting recommendations, and predictive analytics.

---

# Key Features

* Historical NHL fixture browser
* Moneyline betting simulation
* Historical sportsbook odds integration
* Bankroll management
* Betting history
* Team information pages
* Season statistics
* Historical game search and filtering

Future Enhancements:

* Expected Value (EV) calculations
* Kelly Criterion staking recommendations
* Elo Rating System
* Betting recommendation engine
* Advanced analytics dashboard
* Historical backtesting

---

# Technical Approach

**Frontend**

* Python
* Streamlit

**Backend**

* Python

**Database**

* MySQL (data engineering and SQL joins)
* SQLite (application database)
* CSV datasets

**Data Processing**

* Pandas
* SQL

**Data Collection**

* Custom Python web scraper for historical sportsbook odds

---

# Success Metrics

* Successful simulation of an entire historical NHL season.
* Accurate bankroll calculations.
* Persistent betting history using SQLite.
* Correct integration of historical NHL data with sportsbook odds.
* Responsive user interface for browsing fixtures and placing bets.
* Modular architecture supporting future analytical and predictive models.

---

# Timeline

### Phase I

* Acquire NHL historical dataset.
* Perform MySQL joins and data preprocessing.
* Develop Python web scraper for historical odds.
* Merge datasets into a simulation-ready dataset.
* Build homepage.
* Develop Fixtures & Bets page.
* Implement bankroll management.
* Implement betting history.

### Phase II

* Implement Expected Value calculations.
* Implement Kelly Criterion.
* Add betting recommendations.

### Phase III

* Develop Elo Rating System.
* Estimate win probabilities.
* Integrate Elo ratings into betting recommendations.

### Phase IV

* Develop analytics dashboard.
* Implement historical backtesting.
* Expand the platform with advanced statistical and predictive models.
