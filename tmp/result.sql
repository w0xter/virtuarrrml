SELECT shape_id AS shapes_shape_id,
shape_pt_sequence AS shapes_shape_id,
shape_pt_lat AS shapes_shape_pt_sequence,
shape_pt_lon AS shapes_wgs84_poslat_shape_pt_lat,
shape_pt_sequence AS shapes_wgs84_poslong_shape_pt_lon FROM SHAPES 
 WHERE shapes_shape_id IS NOT NULL AND 
shapes_shape_id IS NOT NULL AND 
shapes_shape_pt_sequence IS NOT NULL AND 
shapes_wgs84_poslat_shape_pt_lat IS NOT NULL AND 
shapes_wgs84_poslong_shape_pt_lon IS NOT NULL ;
