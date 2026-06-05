# Unit Converter — Product Requirements Document (PRD)

| 항목 | 내용 |
|------|------|
| 문서 버전 | 0.1 (초안) |
| 작성일 | 2026-06-05 |
| 상태 | Draft |
| 관련 문서 | [README.md](../README.md), [01.UnitConverter_Spec_Report.md](../Report/01.UnitConverter_Spec_Report.md) |

---

## 1. 개요

### 1.1 목적

사용자가 입력한 길이 값(`단위:값`)을 기반으로, 해당 값을 **등록된 모든 길이 단위**로 변환하여 출력하는 CLI 기반 Unit Converter를 제공한다. 레거시 단일 스크립트(`UnitConverter.py`)를 OCP/SRP를 만족하는 패키지 구조로 리팩터링하는 것을 목표로 한다.

### 1.2 배경

현재 코드는 meter/feet/yard 3단위 변환의 기본 흐름만 동작한다. README에 정의된 품질 요구(OCP, SRP, 입력 검증)와 추가 요구(설정 외부화, 동적 단위 등록, 출력 포맷)는 미구현 상태이다.

### 1.3 이해관계자

| 역할 | 관심사 |
|------|--------|
| 실습 참여자 | OCP/SRP 학습, 테스트 작성, AI 활용 실습 |
| 리뷰어 | 설계 원칙 준수, 테스트 커버리지, 확장성 |
| 사용자 | 정확한 변환, 명확한 오류 메시지, 다양한 출력 형식 |

### 1.4 범위

**In Scope**

- `단위:값` 형식 변환 CLI
- meter, feet, yard 기본 단위 및 확장 가능한 단위 레지스트리
- 입력 검증 (형식, 음수, 미등록 단위)
- 외부 설정(JSON/YAML)에서 변환 비율 로드
- 런타임 단위 등록 (`1 cubit = 0.4572 meter`)
- 출력 포맷: 표(table) / JSON / CSV
- 단위·통합 테스트

**Out of Scope**

- GUI / Web UI
- 길이 이외 물리량(질량, 온도 등) 변환
- 다국어(i18n) UI
- 영구 저장(DB, 파일 기록)

---

## 2. 사용자 시나리오

### 2.1 기본 변환

```
입력: meter:2.5
출력 (표 형식 예시):
  2.5 meter = 2.5 meter
  2.5 meter = 8.2 feet
  2.5 meter = 2.7 yard
```

### 2.2 동적 단위 등록 후 변환

```
입력: 1 cubit = 0.4572 meter
→ cubit 단위 등록

입력: cubit:10
출력: 등록된 모든 단위로 변환 결과
```

### 2.3 오류 입력

| 입력 | 기대 동작 |
|------|-----------|
| `meter2.5` | 형식 오류 메시지 |
| `meter:-1` | 음수 오류 메시지 |
| `inch:1` | 미등록 단위 오류 메시지 |

---

## 3. 비즈니스 규칙

| ID | 규칙 |
|----|------|
| BR-01 | **기준 단위(base unit)** 는 `meter` 이다. |
| BR-02 | `1 meter = 3.28084 feet` |
| BR-03 | `1 meter = 1.09361 yard` |
| BR-04 | feet ↔ yard 등 파생 단위 간 변환은 **meter를 허브**로 계산한다. |
| BR-05 | 등록된 단위마다 `1 {unit} = {ratio} meter` 형태의 비율을 갖는다. |
| BR-06 | 길이 값은 **0 이상**만 허용한다 (음수 불가). |
| BR-07 | 표 형식 출력 시 소수 **1자리 반올림** (README 예시 기준). JSON/CSV는 정책에 따라 full precision 또는 동일 자릿수 적용. |

---

## 4. 기능 요구사항 (FR)

| ID | 우선순위 | 요구사항 | 수용 기준 |
|----|----------|----------|-----------|
| FR-01 | P0 | `단위:값` 형식 입력을 파싱한다. | `meter:2.5` → unit=`meter`, value=`2.5` |
| FR-02 | P0 | 입력값을 **등록된 모든 단위**로 변환한다. | 3단위 등록 시 3건 결과 반환 |
| FR-03 | P0 | 초기 지원 단위: meter, feet, yard | 설정 또는 기본값으로 제공 |
| FR-04 | P0 | meter 허브 기준 변환 알고리즘 | BR-01~04 준수 |
| FR-05 | P0 | 단위 추가 시 핵심 변환 코드 수정 없이 확장 | 새 단위는 Registry/설정만 변경 |
| FR-06 | P1 | 변환 비율을 JSON/YAML 설정 파일에서 로드 | `config/units.json` 수정만으로 비율 변경 |
| FR-07 | P1 | 런타임 단위 등록 | `1 cubit = 0.4572 meter` 입력 후 변환 가능 |
| FR-08 | P1 | 출력 포맷 선택 (table / JSON / CSV) | CLI 옵션 또는 프롬프트로 선택 |
| FR-09 | P0 | 변환 정확성 단위 테스트 | 알려진 비율 대비 오차 허용 범위 내 |
| FR-10 | P0 | 입력 검증 단위 테스트 | NFR-03~05 케이스 전부 커버 |

---

## 5. 비기능 요구사항 (NFR)

| ID | 분류 | 요구사항 | 수용 기준 |
|----|------|----------|-----------|
| NFR-01 | 설계 | **OCP** — 확장에는 열려 있고 수정에는 닫혀 있음 | 단위·포맷·설정 로더 추가 시 domain/converter 수정 불필요 |
| NFR-02 | 설계 | **SRP** — 클래스별 단일 책임 | Parser, Validator, Converter, Formatter, UseCase 분리 |
| NFR-03 | 품질 | 음수 입력 거부 | `value < 0` 시 명확한 오류 |
| NFR-04 | 품질 | 잘못된 형식 거부 | 콜론 없음, 빈 unit, 비숫자 value 처리 |
| NFR-05 | 품질 | 미등록 단위 거부 | Registry에 없는 unit명 오류 |
| NFR-06 | 테스트 | I/O와 도메인 분리 | domain/application 계층은 mock I/O 없이 단위 테스트 가능 |
| NFR-07 | 유지보수 | 의존성 방향 | domain ← application ← cli; domain은 outer layer 미참조 |

---

## 6. 아키텍처 개요

### 6.1 패키지 구조

```
unit_converter/
├── domain/           # 변환 규칙, Registry, Models
├── application/      # UseCase (변환, 단위 등록)
├── input/            # Parser, Validator
├── output/           # Table/JSON/CSV Formatter
├── infrastructure/   # Config Loader (JSON/YAML)
└── cli/              # 진입점, I/O

config/units.json
tests/unit/, tests/integration/
```

### 6.2 FR/NFR 레이어 매핑

| 레이어 | FR | NFR |
|--------|----|-----|
| domain | FR-03, FR-04, FR-05, FR-07 | NFR-01, NFR-02 |
| input | FR-01, FR-07(문법) | NFR-02~05 |
| application | FR-02, FR-07(흐름) | NFR-06 |
| infrastructure | FR-06 | NFR-01 |
| output | FR-08 | NFR-01, NFR-02 |
| cli | FR-01, FR-02, FR-08 | NFR-02, NFR-06 |
| tests | FR-09, FR-10 | NFR-01~07 회귀 방지 |

상세 설계는 [01.UnitConverter_Spec_Report.md](../Report/01.UnitConverter_Spec_Report.md) §4 참조.

---

## 7. 인터페이스 명세 (초안)

### 7.1 변환 입력

| 항목 | 값 |
|------|-----|
| 형식 | `{unit}:{value}` |
| 예시 | `meter:2.5` |
| unit | Registry에 등록된 문자열, trim 적용 |
| value | 0 이상의 float |

### 7.2 단위 등록 입력

| 항목 | 값 |
|------|-----|
| 형식 | `1 {unit} = {ratio} meter` |
| 예시 | `1 cubit = 0.4572 meter` |

### 7.3 설정 파일 (JSON)

```json
{
  "base_unit": "meter",
  "units": {
    "meter": 1.0,
    "feet": 3.28084,
    "yard": 1.09361
  }
}
```

> `units` 값: 1 해당 단위 = N meter

### 7.4 CLI (초안)

```bash
python -m unit_converter
python -m unit_converter --format json
python -m unit_converter --config config/units.yaml
```

---

## 8. 오류 처리

| 코드 | 조건 | 사용자 메시지 (예) |
|------|------|-------------------|
| ERR_FORMAT | `:` 없음, 빈 unit | Invalid format. Use unit:value (ex: meter:2.5) |
| ERR_NUMBER | value 비숫자 | Invalid number: {value_str} |
| ERR_NEGATIVE | value < 0 | Value must be zero or positive |
| ERR_UNKNOWN_UNIT | Registry 미등록 | Unknown unit: {unit} |
| ERR_REGISTRATION | 등록 문법 오류 | Invalid registration format |

---

## 9. 테스트 요구사항

| 영역 | 필수 TC |
|------|---------|
| 변환 | meter→feet, feet→meter, yard↔feet (meter 허브) |
| 검증 | 음수, 콜론 없음, unknown unit, 빈 unit |
| 설정 | JSON 로드, YAML 로드 |
| 등록 | cubit 등록 후 변환 |
| 출력 | table/json/csv 스냅샷 또는 구조 검증 |

---

## 10. 구현 단계 (Activities 매핑)

| 단계 | README Activity | 산출물 |
|------|-----------------|--------|
| 1 | 문제 코드 분석 | Spec Report, PRD (본 문서) |
| 2 | 기본·품질 요구 구현 | domain, input, application, cli |
| 3 | TC 구현 | tests/unit |
| 4 | 추가 요구 구현 | infrastructure, output, FR-06~08 |
| 5 | 회고·발표 | 달성도 체크리스트 |

---

## 11. 성공 지표

- [ ] FR-01~05 전항목 수용 기준 충족
- [ ] NFR-01~05 설계 리뷰 통과
- [ ] FR-06~08 추가 요구 구현 및 TC 통과
- [ ] `pytest` 전체 green
- [ ] 단위 추가 시 `domain/converter.py` 변경 없음 확인

---

## 12. 변경 이력

| 버전 | 일자 | 변경 내용 |
|------|------|-----------|
| 0.1 | 2026-06-05 | 초안 작성 (레거시 분석·설계 논의 반영) |
