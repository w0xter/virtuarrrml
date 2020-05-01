(SELECT route_id AS routes_route_id,
route_long_name AS routes_route_long_name FROM ROUTES 
 WHERE routes_route_id IS NOT NULL AND 
routes_route_long_name IS NOT NULL )
 JOIN (SELECT trip_id AS trips_trip_id,
trip_short_name AS trips_trip_short_name FROM TRIPS 
 WHERE trips_trip_id IS NOT NULL AND 
trips_trip_short_name IS NOT NULL )
 JOIN (SELECT trip_id AS stoptimes_trip_id,
stop_id AS stoptimes_trip_id,
arrival_time AS stoptimes_trip_id,
arrival_time AS stoptimes_stop_id FROM STOP_TIMES 
 WHERE stoptimes_trip_id IS NOT NULL AND 
stoptimes_trip_id IS NOT NULL AND 
stoptimes_trip_id IS NOT NULL AND 
stoptimes_stop_id IS NOT NULL )
 JOIN (SELECT stop_id AS stops_stop_id,
stop_name AS stops_stop_name,
wheelchair_boarding AS stops_wheelchair_boarding FROM STOPS 
 WHERE stops_stop_id IS NOT NULL AND 
stops_stop_name IS NOT NULL AND 
stops_wheelchair_boarding IS NOT NULL )
;