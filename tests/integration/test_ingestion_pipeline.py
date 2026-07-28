"""Reproduction test for issue #18.

Minimal test, not the full end-to-end test. A brand new profile gets
reported as "already ingested" and no parsing/chunking/embedding runs.

Cause: pipeline.py _check_skip() calls db_session.query("IngestedSource"),
a string, not the model class. On a mocked db_session, .first() returns
a truthy Mock, so it always looks like a match was found.

TODO (Week 9): the real end-to-end test will need to configure db_session's
mock explicitly (e.g. .first.return_value = None) to work around this, rather
than fixing _check_skip() itself, that stays out of scope for this issue.
"""

from pathlib import Path
from unittest.mock import Mock

import pytest

from ingestion.embeddings.provider import MockEmbeddingProvider
from ingestion.pipeline import IngestionPipeline

FIXTURE_PATH = Path(__file__).parent.parent / "fixtures" / "sample_resumes" / "resume.txt"


@pytest.mark.integration
def test_ingest_resume_end_to_end() -> None:
    resume_text = FIXTURE_PATH.read_text()

    pipeline = IngestionPipeline(
        vector_db=Mock(),
        db_session=Mock(),
        embedding_provider=MockEmbeddingProvider(),
    )

    result = pipeline.ingest_resume(
        profile_id="test-profile",
        content=resume_text,
        filename="resume.txt",
    )

    assert result.skipped is False
    assert result.chunk_count > 0
