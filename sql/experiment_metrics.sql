-- Adapt this template to a warehouse table with one row per experiment user.
-- Primary metric: Day-7 retention. Guardrail: engagement volume.
WITH experiment_population AS (
    SELECT
        user_id,
        experiment_variant,
        CASE WHEN active_on_day_1 THEN 1 ELSE 0 END AS retention_1,
        CASE WHEN active_on_day_7 THEN 1 ELSE 0 END AS retention_7,
        game_rounds_14d
    FROM analytics.experiment_users
    WHERE experiment_name = 'first_gate_placement'
)
SELECT
    experiment_variant,
    COUNT(*) AS users,
    AVG(retention_1) AS retention_1_rate,
    AVG(retention_7) AS retention_7_rate,
    AVG(game_rounds_14d) AS avg_game_rounds,
    APPROX_QUANTILES(game_rounds_14d, 100)[OFFSET(50)] AS median_game_rounds
FROM experiment_population
GROUP BY 1
ORDER BY 1;

