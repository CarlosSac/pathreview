## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/18

**Issue title:** Add end-to-end ingestion test with a sample resume fixture
#18

**Tier:** [ ] Tier 1 [x] Tier 2 [ ] Tier 3

**Why this issue is right for me:** I've worked on unfamiliar codebases before, so a Tier 2 issue that spans a couple of modules is a reasonable step. I already located and read the exact code the issue touches (`ingest_resume()` in `pipeline.py`, and the existing parser tests), and I can trace the flow well enough to plan the test without guessing. There are no blockers on the issue, and I feel confident that I will be able to finish before the week 9 deadline.

**Problem summary:**
Right now the codebase only tests parsers in isolation. There's no test that checks the whole resume upload process work from start to finish. When someone uploads a resume, it's supposed to get parsed, split into chunks, turned into embeddings, and saved to the database, but nothing currently verifies all of those steps actually work together correctly. The tests/integration/ folder is empty, and there isn't a sample resume file set up to test with yet. Fixing this means writing a new test that uploads a real sample resume and checks it makes it all the way through the pipeline successfully. Also, there needs to be a sample resume file for the test to use. This issue/feature mainly in the ingestion pipeline code and the test folders. While reviewing the pipeline, I also noticed the database-recording step is still a placeholder and doesn't actually save anything yet, so I'm scoping my test to the parts that are implemented rather than testing against that unfinished part.

**Branch name:** test/18-ingestion-pipeline-integration

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger

Add this section below your Week 7 entry in JOURNAL.md. Do not replace your previous entry!

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** https://github.com/CarlosSac/pathreview/commit/606b10e22808fe0f1049ae241f6223e0f428f270

**Reproduction summary:**
I ran ingest_resume() with a mocked db_session, the same way the existing unit tests mock it, and it reported skipped=True, chunk_count=0 on a brand new profile that had never been ingested before. Nothing was actually parsed, chunked, or embedded. I traced this to \_check_skip() in pipeline.py, which queries db_session.query("IngestedSource") using a string instead of the actual model class, so a mocked session always returns a truthy result and the pipeline thinks a match already exists.

**PLAN.md link:** https://github.com/CarlosSac/pathreview/blob/test/18-ingestion-pipeline-integration/PLAN.md

**Walkthrough video (recommended):** Not recorded this week.

**Blockers or open questions:**
Still deciding whether to work around the `_check_skip()` bug by configuring the mock explicitly in the test, or fix it directly in `pipeline.py`. Leaning toward the workaround, since it keeps this PR scoped to adding a test rather than fixing an unrelated pipeline bug, but open to feedback on that call before I start Week 9.
