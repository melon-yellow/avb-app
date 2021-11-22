DELETE
FROM [iba_db].[dbo].[deFile]
WHERE _timestamp < (
    (
        SELECT MAX(_timestamp)
        FROM [iba_db].[dbo].[deFile]
    ) - 2
)