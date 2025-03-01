// Create storage integration object
create or replace storage integration s3_int
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = S3
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::1234567891012:role/glue_pipeline'
  STORAGE_ALLOWED_LOCATIONS = ('s3://principles-of-datascience/weather-data/')
  COMMENT = 'Integration with aws s3 buckets';

// Get external_id and update it in S3
DESC integration s3_int;

CREATE SCHEMA IF NOT EXISTS PORTFOLIO.SNOWPIPE;

// Create file format object CSV
CREATE OR REPLACE file format PORTFOLIO.SNOWPIPE.csv_fileformat
    type = csv
    field_delimiter = ','
    skip_header = 1
    empty_field_as_null = TRUE
    error_on_column_count_mismatch=false
    ;

// Create stage object with integration object & file format object
CREATE OR REPLACE STAGE PORTFOLIO.SNOWPIPE.aws_s3_csv
    URL = 's3://principles-of-datascience/weather-data/'
    STORAGE_INTEGRATION = s3_int
    FILE_FORMAT = PORTFOLIO.SNOWPIPE.csv_fileformat;

//Listing files under your s3 buckets
list @PORTFOLIO.SNOWPIPE.aws_s3_csv;

// Use Copy command to load the files
COPY INTO PORTFOLIO.WEATHER_DATA.WEATHER_DATA
    FROM @PORTFOLIO.SNOWPIPE.aws_s3_csv
    PATTERN = '.*history_weather_daily_data.*'
    ON_ERROR = 'CONTINUE';

//Validate the data
SELECT * FROM PORTFOLIO.WEATHER_DATA.WEATHER_DATA;
-- TRUNCATE TABLE PORTFOLIO.WEATHER_DATA.WEATHER_DATA;

// Create a pipe
CREATE OR REPLACE pipe PORTFOLIO.SNOWPIPE.WEATHER_DATA_PIPE
AUTO_INGEST = TRUE
AS
COPY INTO PORTFOLIO.WEATHER_DATA.WEATHER_DATA
FROM @PORTFOLIO.SNOWPIPE.aws_s3_csv
pattern = '.*history_weather_daily_data.*'
ON_ERROR = 'CONTINUE';

// Describe pipe to get ARN
DESC pipe WEATHER_DATA_PIPE;