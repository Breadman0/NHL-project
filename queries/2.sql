SELECT 
    g.game_id,
    DATE(g.date_time)        AS date,
    ht.teamName              AS home_team,
    at.teamName              AS away_team,
    g.home_goals,
    g.away_goals,
    CASE 
        WHEN g.outcome = 'home' THEN ht.teamName
        WHEN g.outcome = 'away' THEN at.teamName
        ELSE 'N/A'
    END                      AS winner,
    g.venue
FROM game g
JOIN team_info ht ON g.home_team_id = ht.team_id
JOIN team_info at ON g.away_team_id = at.team_id
WHERE g.season = 20152016
ORDER BY g.date_time;

SELECT * FROM game LIMIT 5

SELECT 
    g.game_id,
    DATE(g.date_time_GMT)    AS date,
    ht.teamName              AS home_team,
    at.teamName              AS away_team,
    g.home_goals,
    g.away_goals,
    CASE 
        WHEN g.outcome = 'home' THEN ht.teamName
        WHEN g.outcome = 'away' THEN at.teamName
        ELSE 'N/A'
    END                      AS winner,
    g.venue
FROM game g
JOIN team_info ht ON g.home_team_id = ht.team_id
JOIN team_info at ON g.away_team_id = at.team_id
WHERE g.season = 20152016
ORDER BY g.date_time_GMT;








CREATE TABLE MOCK AS
SELECT 
	game_id,
    DATE(date_time_GMT) AS date,
    ht.teamName as home_team,
    a.teamName as away_team,
    home_goals,
    away_goals,
    venue,
    CASE
		WHEN g.outcome = 'home win REG' or g.outcome ='home win OT' THEN ht.teamName
        WHEN g.outcome ='away win REG' or g.outcome ='away win OT' then a.teamName
        ELSE 'NaN'
        END AS WINNER
FROM game g
JOIN team_info ht on ht.team_id = g.home_team_id
JOIN team_info a on a.team_id = g.away_Team_id
WHERE g.season = 20182019
ORDER BY g.date_time_GMT


USE  NHL;
SELECT *
FROM nhl_historical_odds

;
CREATE TABLE MOCK AS
SELECT 
    game_id,
    -- Handle the ISO 'T' and 'Z' characters explicitly
    DATE(STR_TO_DATE(g.date_time_GMT, '%Y-%m-%dT%H:%i:%sZ')) AS date,
    ht.teamName as home_team,
    a.teamName as away_team,
    home_goals,
    away_goals,
    venue,
    CASE
        WHEN g.outcome = 'home win REG' or g.outcome ='home win OT' THEN ht.teamName
        WHEN g.outcome ='away win REG' or g.outcome ='away win OT' then a.teamName
        ELSE 'NaN'
    END AS WINNER
FROM game g
JOIN team_info ht on ht.team_id = g.home_team_id
JOIN team_info a on a.team_id = g.away_Team_id
WHERE g.season = 20182019
-- Use the cleaned date parsing format for ordering as well
ORDER BY STR_TO_DATE(g.date_time_GMT, '%Y-%m-%dT%H:%i:%sZ');


SELECT * FROM nhl_historical_odds 


select * from mock
where id = 1321
ALTER TABLE nhl_historical_odds
ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST;


SELECT *
from merged_og