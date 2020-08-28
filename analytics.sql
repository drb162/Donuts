--QUESTION 1
SELECT 
  COUNT(DISTINCT CONCAT( fullvisitorid, visitId ) ) AS distinct_sessions,
FROM `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export`;


--QUESTION 2
SELECT 
    AVG( unique_session_count ) AS avg_sessions_per_user
FROM (
  SELECT
    fullvisitorid, 
    COUNT( DISTINCT visitId ) AS unique_session_count,
  FROM `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export`
  GROUP BY 
    fullvisitorid
)

--QUESTION 3
SELECT AVG (time) / 60000 AS avg_time_in_mins
FROM `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export` t, t.hit
WHERE eventCategory in ('ios.order_confirmation', android.order_confirmation);

--QUESTION 4
WITH 
  analytics1 AS(
    SELECT *, 
      FROM (
        SELECT
          fullvisitorid,
          visitId,
          hitNumber,
          eventCategory, 
          eventAction, 
          eventLabel,
          ROW_NUMBER() OVER (PARTITION BY fullvisitorid, visitId ORDER BY hitNumber DESC) AS seqnum
        FROM `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export` t, t.hit
        WHERE eventAction IN ('address_update.submitted', 'address.submitted') 
      ) 
    WHERE seqnum = 1
  ), 

  analytics2 AS (
    SELECT 
        fullvisitorid,
        visitId,
        transactionId
      FROM `dhh-analytics-hiringspace.GoogleAnalyticsSample.ga_sessions_export` t, t.hit
      WHERE transactionId IS NOT NULL
  )

SELECT
  ga1.fullvisitorid,
  ga1.visitId,
  hitNumber,
  CASE
    WHEN eventCategory = 'ios.checkout' THEN True
    WHEN eventCategory = 'android.checkout' THEN True
    ELSE False
  END AS lateAddressChange,
  eventAction, 
  eventLabel,
  transactionId, 
  CASE 
    WHEN status_id = 24 THEN True
    WHEN status_id IS NULL THEN NULL
    ELSE False
  END as successfulDelivery,
  declinereason_code, 
  declinereason_type, 
  geopointCustomer, 
  geopointDropoff, 
  ST_DISTANCE(geopointCustomer, geopointDropoff)
FROM analytics1 ga1
LEFT JOIN analytics2 ga2 ON
  ga1.fullvisitorid = ga2.fullvisitorid AND
  ga1.visitId = ga2.visitId
LEFT JOIN `dhh-analytics-hiringspace.BackendDataSample.transactionalData` be ON
  ga2.transactionId = be.frontendOrderId;
