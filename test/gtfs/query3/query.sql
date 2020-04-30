SELECT stop_id AS stops_stop_id,
stop_desc AS stops_description_stop_desc,
stop_lat AS stops_wgs84_poslat_stop_lat,
stop_lon AS stops_wgs84_poslong_stop_lon,
wheelchair_boarding AS stops_termswheelchairAccessible_wheelchair_boarding FROM STOPS 
 WHERE stops_stop_id IS NOT NULL ;
