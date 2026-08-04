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

**Reproduction commit link:** https://github.com/CarlosSac/pathreview/commit/60d20d18121fa7bb694da07d8692905075ede5a7

**Reproduction summary:**
I ran ingest_resume() with a mocked db_session, the same way the existing unit tests mock it, and it reported skipped=True, chunk_count=0 on a brand new profile that had never been ingested before. Nothing was actually parsed, chunked, or embedded. I traced this to \_check_skip() in pipeline.py, which queries db_session.query("IngestedSource") using a string instead of the actual model class, so a mocked session always returns a truthy result and the pipeline thinks a match already exists.

**PLAN.md link:** https://github.com/CarlosSac/pathreview/blob/test/18-ingestion-pipeline-integration/PLAN.md

**Walkthrough video (recommended):** Not recorded this week.

**Blockers or open questions:**
Still deciding whether to work around the `_check_skip()` bug by configuring the mock explicitly in the test, or fix it directly in `pipeline.py`. Leaning toward the workaround, since it keeps this PR scoped to adding a test rather than fixing an unrelated pipeline bug, but open to feedback on that call before I start Week 9.

## Week 9 — Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**
3 of 5 tasks from PLAN.md are done. I fixed the mock setup so the test gets past the pipeline bug and actually passes now. I added a check that embeddings really get stored, not just chunked. I also added a second sample resume (one with no work experience section) and a test for it.

**Next steps:**
Add a test for the "skip if already ingested" case, and then clean up the test file and make sure everything passes before opening a PR.

**Blockers:**
None right now.

---

### Check-in 2 (end of week)

**PR link:** https://github.com/ascherj/pathreview/pull/810

**Branch:** `test/18-ingestion-pipeline-integration`

**What you built:**
An end-to-end integration test suite for the resume ingestion pipeline (parse, chunk, embed, store), using sample resume fixtures. Along the way I found and documented a real bug in the pipeline's already-ingested check, and worked around it in the tests rather than fixing the pipeline itself, since that's out of scope for this issue.

**Tests added or updated:**
Added `tests/integration/test_ingestion_pipeline.py` with 3 tests: the full ingestion flow on a normal resume, the same flow on a resume with no work experience section, and the already-ingested skip path. Added two fixtures in `tests/fixtures/sample_resumes/` (`resume.txt`, `resume_no_experience.txt`).

**Self-review confirmation:** [x] make check passes [x] make test-unit passes
(Both have pre-existing failures/errors unrelated to this change, documented in the PR's Notes for Reviewers. Confirmed via `git diff --stat main...HEAD` that none of the affected files were touched here, and verified under a clean Python 3.11 environment per SETUP.md.)

**Draft PR feedback received from:** none

3 of 5 tasks from PLAN.md are done. I configured the mocked `db_session` in the test so it gets past the `_check_skip()` bug without touching `pipeline.py` (sub-task 1), which turned the Week 8 reproduction test into a real passing test. I added an assertion that `vector_db.add` is actually called once per chunk, proving embeddings are stored, not just that chunking happened (sub-task 2). I also added a second fixture resume with no work experience section, mirroring the existing case in `test_resume_parser.py`, plus a test confirming the pipeline still produces chunks for it (sub-task 3).

**Next steps:**
Sub-task 4: add a test for the skip path itself, ingesting the same resume twice and asserting the second call reports `skipped=True`, since the workaround from sub-task 1 otherwise means that behavior is never tested by anything. Then sub-task 5: clean up the test file's docstring/naming now that it's the real test suite, not just a reproduction, and confirm the full suite passes green before opening a PR.
