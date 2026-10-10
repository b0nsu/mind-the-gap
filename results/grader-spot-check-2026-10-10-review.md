# 여섯 번째 채점 검수 결과 — 2026-10-10

검수자: claude-opus-5-5. 사람 검수가 아닙니다. 채점자(`grade3.py`, 도구 호출을 봄)도 claude-opus-5-5라서 앞의 다섯 검수보다 독립성이 약합니다. 샘플 `grader-spot-check-2026-10-10-human.md`(skill 1.3.0, eval set 1.5.0, 15건, 단언문 60개)를 정답표 없이 채운 뒤 `grader-spot-check-2026-10-10-human-KEY.md`와 대조했습니다. 채운 시트는 `grader-spot-check-2026-10-10-opus-seat.md`입니다. 원본 `-human.md`는 사람 검수용으로 비워 두었습니다.

결과: 60개 중 56개 일치. 불일치 4개는 모두 채점자가 더 엄격한 쪽입니다. 검수자가 단언문 문제로 표시한 H14-4는 채점자와 판정이 같습니다.

| 샘플 | 단언문 | 검수자 | 채점자 | 비고 |
|---|---|---|---|---|
| H02 | 3 | P | F | 응답에 결과(consequence) 문장이 없음. 검수자는 "같은 결과를 다시 설명하지 않는다"를 공허하게 참으로 봤고, 채점자는 근거 없음으로 실패 처리. 단언문이 이 경우를 정하지 않음 → `fault_candidates` 15#3. 스킬 없는 run. |
| H08 | 2 | P | F | "Before you commit to Notion, check whether your team uses Jira"를 검수자는 조건으로, 채점자는 응답 자신의 진행·중단 조건이 아니라고 봄. 경계. 채점자 읽기가 단언문 예시('if you don't use Jira, I'll go ahead')에 더 가까움. |
| H13 | 2 | P | F | 마지막 응답 첫 문장 "It does not yet work across all three servers"와 마지막 불릿이 같은 충돌을 말함. 검수자는 요약과 상술로, 채점자는 반복으로 봄. 09b H04-5와 같은 종류의 경계. |
| H15 | 3 | P | F | "This can't be undone"이 삭제 뒤에 나옴. 단언문은 시점을 정하지 않고, 채점자는 기대 행동(실행 전 결과 진술)을 적용 → `fault_candidates` 9#3. 스킬 없는 run. 같은 run의 1·4는 채점자와 검수자 모두 실패. |

검수자가 경계로 본 자리 중 H04-3(Sonnet, 스킬 없음, 바꿔야 할 조건을 "If the deployment stays as described, swapping this module for Postgres is a small change"로 말함)과 H14-4(기본값 없는 "Who owns this?")는 채점자와 판정이 같습니다.

여섯 검수 합계: 358개 중 불일치 22개. 20개는 채점자가 더 엄격한 쪽, 2개는 검수자가 더 엄격한 쪽. 여섯 번째는 1.3.0 표에서 뽑은 첫 샘플입니다. 세 번째부터 다섯 번째는 1.2.1 표의 같은 63개 샘플이었습니다. 사람의 독립 채점은 아직 없습니다. 2026-10-10 유지보수자가 이 60개 판정과 불일치 4건을 정답표·run과 함께 읽고 전부 채점자 쪽에 동의했습니다. 판정 검토이지 독립 채점은 아닙니다.
