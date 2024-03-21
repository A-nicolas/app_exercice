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