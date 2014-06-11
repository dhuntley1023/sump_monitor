/*
** Table: samples
**
** Contians log of water depth readings on a per-minute basis
*/
CREATE TABLE IF NOT EXISTS samples (
	sample_time CHAR PRIMARY KEY, -- Format YYYY-MM-DD HH:MM
	depth REAL  -- Units: Inches
);

CREATE UNIQUE INDEX IF NOT EXISTS sample_time ON samples (sample_time);	


/*
** Table: hourly_summaries
**
** Hourly summary of sump pump activity
*/
CREATE TABLE IF NOT EXISTS hourly_summaries (
	sample_time CHAR PRIMARY KEY,  -- Format YYYY-MM-DD HH:00
	num_drainings INT, -- Number of times the sump pump activated
	gallons_drained REAL  -- Number of gallons that were drained
);

