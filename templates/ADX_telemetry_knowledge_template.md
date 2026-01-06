# Azure Data Explorer (ADX) Dashboard (Telemetry) Knowledge

## 1. Overview 

### 1.1. Product Overview 

- **Product**: <PRODUCT_NAME> 
- **Description**: <PRODUCT_DESCRIPTION> 
- **Abbreviation**: <LIST_OF_PRODUCT_ABBREVIATION>

---


# OKR(KR) Knowledge 

## 1. Overview 

- <NAME_OF_OKR_1>: <WHAT_THIS_OKR_IS_USED_FOR>
- <NAME_OF_OKR_2>: <WHAT_THIS_OKR_IS_USED_FOR>
- ...

## 2. OKRs

### 2.1. OKR: <NAME_OF_OKR_1>

- **OKR Name**: <NAME_OF_OKR_1>
- **Description**: <WHAT_THIS_OKR_IS_USED_FOR>

#### 2.1.1. Primary Query and Filters

##### 2.1.2.1. Primary Query 

- **Cluster**: <Default_Kusto_Cluster>
- **Database**: <Default_Database_Name>

```kql
<Primary_Query>
```

##### 2.1.2.2. Filters

Specify the filters defined as variable in the primary query and their default values that are always applied when computing the OKR. 

| Filters | Type | Values | Default Values for OKR | Notes | IsAnalysisDimension |
|--------:|:-----|:-------|:-----------------------|:------|:--------------------|
| <TIMESTAMP_FILTER> | <TYPE> | - | startofday(now()) | Primary time filter used for time-series analysis and windowing. | No |
| <USER_TYP_FILTER> | <TYPE> | external, internal, total |total | User type used for cohort slicing. | Yes |
| <SCENARIO_TYPE> | <TYPE>  | migrate, upgrade, migrate/update | migrate/update | Scenario / project / template / workflow type used for cohort slicing. | Yes |

Notes:
- If a filter is tagged Yes in `IsAnalysisDimension`, the filter should be treated as a primary candidate for cohort analysis and can be safely used to break results down into slices (segments) for comparisons across groups.

#### 2.1.3. Targets, Thresholds, and Guardrails

- **Target Value**: <METRIC_NAME> >= <TARGET_VALUE>.
- **Volume Requirements**: Show base volume (e.g., TotalEntities) alongside the metric to confirm that trends are based on sufficient data.

#### 2.1.4. Recommended Breakdowns and Dimensions

By default, it could used any relevant filter which `IsAnalysisDimension` is tagged as `Yes` to slice the OKR for Corhort Analysis. If necessary, suggested analysis dimensions manually here. 

- **Scenario / Template Type** (e.g., ProjectType, ScenarioType):
	- Goal: Identify underperforming scenarios or templates and top performers.
- **Client / Version** (e.g., ClientVersion, AppBuild):
	- Goal: Detect regressions or improvements tied to specific builds or releases.
- **Error / Category** (joined via dimension tables, e.g., ErrorCode, CategoryId):
	- Goal: Understand top failure categories and their prevalence.
- **User / Environment Flags** (e.g., IsInternalUser, Channel, Region):
	- Goal: Separate internal vs external and understand environmental differences.

For each breakdown, document:

- How to interpret high or low values.
- Which cohorts are considered healthy vs risky.

### 2.2. OKR: <NAME_OF_OKR_2>

...

## 3. Notes and Conventions

- Always accompany percentage-based KPIs with their underlying counts.
- Clearly separate **default values for filters** (always on) from **ad-hoc values for filters** (used for explorations only).
- Keep this updated when new queries, or OKRs are introduced so downstream tools and agents can reason accurately about telemetry.
- If any information cannot be gotten from ADX dashboard directly, highlight them and ask user to complete manually.

---


