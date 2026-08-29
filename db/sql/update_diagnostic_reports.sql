-- Update diagnostic_reports to match the DiagnosticReport model in backend/app/models/diagnostic_report.py
-- Expected columns: id, service_call_id, file_url, notes, created_at

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'diagnostic_reports'
          AND column_name = 'timestamp'
    ) AND NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'diagnostic_reports'
          AND column_name = 'created_at'
    ) THEN
        ALTER TABLE diagnostic_reports RENAME COLUMN timestamp TO created_at;
    END IF;
END $$;

ALTER TABLE diagnostic_reports
    ALTER COLUMN created_at TYPE TIMESTAMP USING created_at::TIMESTAMP,
    ALTER COLUMN created_at SET DEFAULT NOW();

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'diagnostic_reports'
          AND column_name = 'service_call_id'
    ) THEN
        ALTER TABLE diagnostic_reports ADD COLUMN service_call_id INTEGER;
    END IF;
END $$;

UPDATE diagnostic_reports
SET service_call_id = 1
WHERE service_call_id IS NULL
  AND EXISTS (SELECT 1 FROM service_calls WHERE id = 1);

ALTER TABLE diagnostic_reports
    ALTER COLUMN file_url SET NOT NULL,
    ALTER COLUMN service_call_id SET NOT NULL;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'diagnostic_reports_service_call_id_fkey'
    ) THEN
        ALTER TABLE diagnostic_reports
            ADD CONSTRAINT diagnostic_reports_service_call_id_fkey
            FOREIGN KEY (service_call_id) REFERENCES service_calls(id);
    END IF;
END $$;

-- Optional: if notes should be required in your app, uncomment the next line.
-- ALTER TABLE diagnostic_reports ALTER COLUMN notes SET NOT NULL;
