SECTIONS = """
SELECT
    TRIM(sec_rec.crs_no) AS crs_no, sec_rec.cat as phile,
    sec_rec.yr, TRIM(sec_rec.sess) AS sess, sec_rec.sec_no,
    sec_rec.subsess,
    TRIM(
        TRIM(crs_rec.title1) || " " ||
        TRIM(crs_rec.title2) || " " ||
        TRIM(crs_rec.title3)
    ) AS crs_title,
    sec_rec.title AS sec_title,
    sec_rec.fac_id, TRIM(id_rec.firstname) AS firstname,
    TRIM(id_rec.lastname) AS lastname,
    TRIM(id_rec.firstname) || ' ' || TRIM(id_rec.lastname) AS fullname,
    CASE
        WHEN
            mtg_rec.im
        IN
            ("LX","LC","ST","TJ","ML","TS","EN","PR")
        THEN
            'Y'
        END
    AS
        needSyllabi
FROM
    sec_rec
INNER JOIN
    crs_rec
ON
    sec_rec.crs_no = crs_rec.crs_no
AND
    sec_rec.cat = crs_rec.cat
INNER JOIN
    id_rec
ON
    sec_rec.fac_id = id_rec.id
INNER JOIN
    secmtg_rec
ON
    sec_rec.crs_no = secmtg_rec.crs_no
AND
    sec_rec.cat = secmtg_rec.cat
AND
    sec_rec.yr = secmtg_rec.yr
AND
    sec_rec.sess = secmtg_rec.sess
AND
    sec_rec.sec_no = secmtg_rec.sec_no
INNER JOIN
    mtg_rec
ON
    secmtg_rec.mtg_no = mtg_rec.mtg_no
WHERE
    sec_rec.stat !=  'X'
{where}
ORDER BY
    crs_no, sec_no
""".format
