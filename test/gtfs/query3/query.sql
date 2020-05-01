(SELECT stop_id AS stops_stop_id,
stop_desc AS stops_stop_desc,
stop_lat AS stops_stop_lat,
stop_lon AS stops_stop_lon,
wheelchair_boarding AS stops_wheelchair_boarding,
 FROM STOPS 
 WHERE stops_stop_id IS NOT NULL AND 
stops_stop_lat IS NOT NULL AND 
stops_stop_lon IS NOT NULL AND 
AND (stops_stop_lat > 40.41 ))
