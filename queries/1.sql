CREATE DATABASE NHL;
USE NHL;
SELECT
g.game_id,
h.teamName AS home_team,
a.teamName AS away_team,
g.home_goals,
g.away_goals
FROM game g
JOIN team_info h
ON g.home_team_id = h.team_id
JOIN team_info a
ON g.away_team_id = a.team_id;