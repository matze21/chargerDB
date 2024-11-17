SELECT c.charger_id, ts.price_per_kwh
FROM EV_Chargers c 
JOIN Charger_Schedule_Assignment csa ON c.charger_id = csa.charger_id
JOIN Pricing_Schedules ps ON csa.schedule_id = ps.schedule_id
JOIN Time_Slots ts ON ps.schedule_id = ts.schedule_id
WHERE c.charger_id = 2
  AND CURRENT_DATE BETWEEN csa.effective_from AND csa.effective_to
  AND CURRENT_TIME BETWEEN ts.start_time AND ts.end_time;