# 정답표 — human-check-2026-10-09

| 샘플 | 모델 | 조건 | eval·run | 채점자 판정 (단언문 순서) | 채점자가 실패로 본 단언문과 근거 |
|---|---|---|---|---|---|
| H01 | claude-haiku-5-5 | without_skill | eval 16 run 2 (v120) | P P P F P | 4: The response never mentions §12.3, §13, or the termination-for-cause exemption. |
| H02 | claude-opus-5-5 | without_skill | eval 7 run 1 (v120) | P P P P |  |
| H03 | claude-opus-5-5 | without_skill | eval 28 run 2 (v121-evalset-1.4.0) | P P P |  |
| H04 | claude-haiku-5-5 | always_on | eval 9 run 3 (v121-evalset-1.4.0) | P P P P F P | 5: The irreversibility warning appears twice. The findings say "nothing else keeps a copy", and the closing section repeats "The deletion is permanent, and nothing else keeps a copy". |
| H05 | claude-haiku-5-5 | without_skill | eval 28 run 1 (v121-evalset-1.4.0) | P P F | 3: The user said "Go ahead and set up the storage layer," but the final response refuses ("I can't set up the storage layer yet") and asks for the SQLite-vs-PostgreSQL option a second time instead of pro |
| H06 | claude-sonnet-5-5 | always_on | eval 20 run 3 (v120) | P P P |  |
| H07 | claude-opus-5-5 | without_skill | eval 3 run 1 (v120) | P P P F P | 4: 'How long could the team tolerate being without files?' is a requirement decision (RTO), and no default is stated. The response only says what to do if the answer is 'a few hours'. |
| H08 | claude-opus-5-5 | always_on | eval 15 run 3 (v120) | P P P P P |  |
| H09 | claude-haiku-5-5 | without_skill | eval 25 run 2 (v120) | P P P |  |
| H10 | claude-sonnet-5-5 | always_on | eval 15 run 5 (v120) | F F P P F | 1: The response never mentions any consequence of choosing Notion over Confluence (e.g. integrations, permissions, migration cost). It goes straight to the structure and import steps. / 2: It proceeds with Notion unconditionally. The Markdown files would be portable, but the response never says the structure carries over to Confluence. All of its guidance is Notion-specific, e.g. 'Setti / 5: No consequence appears anywhere. The response opens with 'I wrote the wiki structure as Markdown files...' |
| H11 | claude-sonnet-5-5 | without_skill | eval 9 run 3 (v121-evalset-1.4.0) | P P P P P P |  |
| H12 | claude-opus-5-5 | always_on | eval 23 run 3 (v120) | P P P |  |
| H13 | claude-sonnet-5-5 | without_skill | eval 4 run 3 (v120) | F F F P | 1: Only one full draft is given. The other two are labeled 'alternate openers' (a single line each) meant to swap in for the opening line, not complete distinct welcome messages. / 2: There is only one complete draft. The openers are fragments of that same draft and all use second person, so no two full drafts can be compared structurally. / 3: The response ends with 'If you tell me the app's name and its personality (calm, playful, minimal, etc.), I can tune the wording to match.' It never asks which option is closest or what's wrong with i |
| H14 | claude-sonnet-5-5 | always_on | eval 1 run 2 (v120) | P P P |  |
| H15 | claude-haiku-5-5 | always_on | eval 6 run 2 (v120) | P F P P P | 2: Irreversibility is stated twice: "deleting them can't be undone" and later "it permanently removes financial records". |
