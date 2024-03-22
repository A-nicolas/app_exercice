CREATE TABLE IF NOT EXISTS feedback_data_v2 (
	unique_id STRING,
    bootcampname STRING,
    prioriteRetour STRING,
    typeRetour STRING,
    date_feedback STRING,
    rating STRING,
    comments STRING,
    attachedfiles STRING,
    consentement BOOLEAN,
    is_deleted BOOLEAN
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
STORED AS TEXTFILE
LOCATION '/data/upload/';