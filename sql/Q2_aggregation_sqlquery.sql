-- Vahan Case Study | Q2: Aggregate lead-level raw data to the lead_source (cohort) level
-- Assumes the raw data lives in a table: raw_leads
-- Grain of raw_leads: 1 row per candidate (candidate_phone) per lead_source
CREATE DATABASE VahanCaseStudy;
GO

USE VahanCaseStudy;
GO

SELECT TOP 10 *
FROM raw_leads;

SELECT COUNT(*) AS total_rows
FROM raw_leads;

SELECT
    COLUMN_NAME,
    DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'raw_leads'
ORDER BY ORDINAL_POSITION;

SELECT
    lead_source,

    SUM(uploaded_leads) AS uploaded_leads,
    SUM(attempted) AS attempted,
    SUM(CAST(connected AS INT)) AS connected,
    SUM(CAST(interested AS INT)) AS interested,
    SUM(ob_after_upload) AS ob_after_upload,
    SUM(ft_after_upload) AS ft_after_upload,
    SUM(ft_after_first_attempt) AS ft_after_first_attempt,

    ROUND(
        100.0 * SUM(attempted)
        / NULLIF(SUM(uploaded_leads), 0),
        1
    ) AS attempted_pct,

    ROUND(
        100.0 * SUM(CAST(connected AS INT))
        / NULLIF(SUM(attempted), 0),
        1
    ) AS connect_rate_pct,

    ROUND(
        100.0 * SUM(CAST(interested AS INT))
        / NULLIF(SUM(CAST(connected AS INT)), 0),
        1
    ) AS interested_rate_pct,

    ROUND(
        100.0 * SUM(ft_after_upload)
        / NULLIF(SUM(uploaded_leads), 0),
        2
    ) AS ft_conversion_pct

FROM raw_leads

GROUP BY lead_source

ORDER BY ft_conversion_pct DESC;