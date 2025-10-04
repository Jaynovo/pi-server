CREATE OR REPLACE VIEW state_burgenland AS
Select *
FROM stations s
WHERE state = 'Burgenland'
ORDER BY s.station_id DESC;

CREATE OR REPLACE VIEW state_kntn AS
Select *
FROM stations s
WHERE state = 'Kärnten'
ORDER BY s.station_id DESC;

CREATE OR REPLACE VIEW state_noe AS
Select *
FROM stations s
WHERE state = 'Niederösterreich'
ORDER BY s.station_id DESC;

CREATE OR REPLACE VIEW state_ooe AS
Select *
FROM stations s
WHERE state = 'Oberösterreich'
ORDER BY s.station_id DESC;

CREATE OR REPLACE VIEW state_sbg AS
Select *
FROM stations s
WHERE state = 'Salzburg'
ORDER BY s.station_id DESC;

CREATE OR REPLACE VIEW state_stmk AS
Select *
FROM stations s
WHERE state = 'Steiermark'
ORDER BY s.station_id DESC;

CREATE OR REPLACE VIEW state_tirol AS
Select *
FROM stations s
WHERE state = 'Tirol'
ORDER BY s.station_id DESC;

CREATE OR REPLACE VIEW state_vbg AS
Select *
FROM stations s
WHERE state = 'Vorarlberg'
ORDER BY s.station_id DESC;

CREATE OR REPLACE VIEW state_wien AS
Select *
FROM stations s
WHERE state = 'Wien'
ORDER BY s.station_id DESC;