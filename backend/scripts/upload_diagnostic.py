"""
uploads a diagnostic report file to s3 using boto3 sdk,
then creates a matching diagnostic row

run from backend with virtual env running 
python -m scripts.upload_diagnostic.py
"""

import asyncio
import boto3

from app.database import AsyncSessionLocal
from app.models import DiagnosticReport

# Keep the bucket name in one place so the upload logic is easy to reuse and
# update without scattering hard-coded environment details across the codebase.
BUCKET_NAME = "bankdemo-diagnostics-jg8070"
# The sample file demonstrates how a diagnostic artifact is stored locally before
# being uploaded for inspection or troubleshooting.
LOCAL_FILE_PATH = "scripts/sample_diagnostic.txt"

# The S3 object key is the path inside the bucket. Storing a predictable path
# allows the app to reconstruct the file URL later and reference the artifact
# from the database.
S3_KEY = "diagnostics/chaseatm.txt"


# Upload the diagnostic report to S3 and return the stored URL. This is
# important because the database can only keep a reference to the file; the file
# itself lives in object storage.
def upload_to_s3() -> str:
    s3_client = boto3.client("s3")
    s3_client.upload_file(LOCAL_FILE_PATH, BUCKET_NAME, S3_KEY)
    return f"s3://{BUCKET_NAME}/{S3_KEY}"


# Save a DiagnosticReport row that links the uploaded file to a service call.
# This makes the artifact discoverable in the app and preserves the connection
# between the report and the issue it documents.
async def record_diagnostic_log(file_url: str) -> None:
    async with AsyncSessionLocal() as session:
        log = DiagnosticReport(
            service_call_id=2,
            file_url=file_url,
            notes="uploaded via upload_diagnostic.py"
        )

        session.add(log)
        await session.commit()
        await session.refresh(log)
        print(f"Created DiagnosticReport id={log.id}, file_url={log.file_url}")


# Run the end-to-end workflow: upload the artifact, then record the metadata in
# the database so future code can show or fetch the file associated with the
# service call.
async def main() -> None:
    file_url = upload_to_s3()
    print(f"Uploaded to {file_url}")
    await record_diagnostic_log(file_url)


if __name__ == "__main__":
    asyncio.run(main())