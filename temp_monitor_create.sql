CREATE TABLE temp_history(
  sample_time,
  temperature
);
CREATE UNIQUE INDEX sample_time on temp_history (sample_time);
