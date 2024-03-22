CREATE TABLE feedback_data_v2 (
    unique_id STRING,
    bootcampname STRING,
    prioriteRetour STRING,
    typeRetour STRING,
    date_feedback STRING,
    rating STRING,
    comments STRING,
    attachedfiles STRING
) STORED AS ORC

CREATE TABLE IF NOT EXISTS feedback_data_v3 (
unique_id STRING,
    bootcampname STRING,
    prioriteRetour STRING,
    typeRetour STRING,
    date_feedback STRING,
    rating INT,
    comments STRING,
    attachedfiles STRING,
    consentement BOOLEAN,
    is_deleted BOOLEAN
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
