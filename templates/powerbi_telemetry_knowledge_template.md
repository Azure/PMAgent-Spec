# Power BI Semantic Model Schema Knowledge

## 1. Overview 

### 1.1. Product Overview 

- **Product**: <PRODUCT_NAME> 
- **Description**: <PRODUCT_DESCRIPTION> 
- **Abbreviation**: <LIST_OF_PRODUCT_ABBREVIATION>

### 1.2. Power BI Semantic Model Schema Overview 

- **Semantic Model**: <NAME_OF_MODEL>
	- **Dashboard/Report**: <LINK_TO_BI_DASHBOARD>
    - **Tables**
        - <NAME_OF_TABLE_1>: <SHORT_PURPOSE_DESC>
	    - <NAME_OF_TABLE_2>: <SHORT_PURPOSE_DESC>
    - **Important Relationships (Conceptual)**:
	    - <FACT_TABLE>.<FOREIGN_KEY> → <DIM_TABLE>.<PRIMARY_KEY> (<CARDINALITY_DESC>)

## 2. Semantic Model Schema

### 2.1. Table: <NAME_OF_TABLE_1>

- **Table Name**: <NAME_OF_TABLE_1>
- **Purpose**: <WHAT_THIS_TABLE_IS_USED_FOR>
- **Semantic Model**: <NAME_OF_MODEL>
- **Dashboard/Report**: <LINK_TO_BI_DASHBOARD>

#### 2.1.1. Columns

| Column          | Type    | Format / Example | Notes | IsAnalysisDimension |
|----------------:|:--------|:-----------------|:------|:------|
| <ID_COLUMN>     | <TYPE>  | —                | Logical identifier of the entity being measured (project, user, session, etc.). | No |
| <CLIENT_NAME>   | <TYPE>  | —                | Name of the client / surface emitting telemetry. | Yes | 
| <CLIENT_VERSION>| <TYPE>  | —                | Version identifier for cohort analysis and regression checks. | Yes | 
| <TIMESTAMP>     | <TYPE>  | <FORMAT>         | Primary time field used for time-series analysis and windowing. | No |
| <DIM_KEY>       | <TYPE>  | —                | Foreign key to dimension table (e.g., error code, category). | No | 
| <FLAGS>         | <TYPE>  | —                | Boolean or enum flags for scenario, experiment, or status (e.g., internal vs external). | Yes | 
| <SCENARIO_TYPE> | <TYPE>  | —                | Scenario / project / template type used for cohort slicing. | Yes |

Notes:
- If a column is tagged Yes in IsAnalysisDimension, the column should be treated as a primary candidate for cohort analysis and can be safely used to break results down into slices (segments) for comparisons across groups.

#### 2.1.2. Measures

| Measure                | Type   | Format           | Description |
|-----------------------:|:-------|:-----------------|:------------|
| <MEASURE_1_NAME>       | <TYPE> | <FORMAT_STRING>  | <WHAT_IT_REPRESENTS> |
| <MEASURE_2_NAME>       | <TYPE> | <FORMAT_STRING>  | <WHAT_IT_REPRESENTS> |

#### 2.1.3. Key Usage Patterns

- Use <TABLE_NAME> as a dimension for breaking down <KPI_OR_VOLUME> by <CATEGORY>.
- Use <MEASURE_NAME> for <KPI_CARD_OR_CONDITIONAL_FORMATTING_USE_CASE>.
- ...

### 2.2. Table: <NAME_OF_TABLE_2>

... 

## 3. Entity Relationships (Conceptual)

Describe the entity relationships among all tables.

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

#### 2.1.1. Time Semantics

- **Default Display Period**: <e.g., Latest 6 full calendar months relative to "today" and end date is strictly before "today">
- **Measurement Window**: <Calendar day | Calendar week | Calendar month | Calendar quarter | Rolling N days | Rolling N weeks / months>
- **Timestamp Field for Aggreation**: <TABLE>[<TIMESTAMP_COLUMN>]


Notes: 
- **Measurement Window Definition** :
    - **Calendar day**: Fixed 24‑hour period using calendar boundaries, e.g., from 00:00 to 23:59 local time (or UTC) for each date.
    - **Calendar week**: Fixed 7‑day period aligned to a consistent start day (e.g., Monday–Sunday), using full calendar weeks; “this week” is from week‑start 00:00 to next week‑start 00:00.
    - **Calendar month**: Fixed period from the first day of a month at 00:00 to the first day of the next month (exclusive). Often used with “completed month” (must be fully elapsed).
    - **Calendar quarter**: Fixed 3‑month period aligned to Q1–Q4 (e.g., Jan–Mar, Apr–Jun, etc.), again using full, completed quarters only.
    - **Rolling N days (e.g., 7‑day, 28‑day, 90‑day)**: Sliding window that always covers the most recent N full days relative to “now” (e.g., last 7 complete days), updating continuously instead of waiting for a period to close.
    - **Rolling N weeks / months**: Similar to rolling N days but expressed in whole weeks or months (e.g., “last 3 completed months”), always anchored relative to the current date.

#### 2.1.2. Telemetry Scope and Filters

##### 2.1.2.1. Scope

- **Primary Tables**: <LIST_OF_TABLES>
- **Join Dimensions** (if relevant): <LIST_OF_JOIN_DIMENSIONS>

##### 2.1.2.2. Global Filters

Specify filters that are always applied when computing the OKR:

- **<FILTER_NAME_1>**: <e.g., `NOT 'OKR_Local_Debug'[IsInternalUser]` to focus on external customers.>
- **<FILTER_NAME_2>**: ...
- ...

#### 2.1.3. Metric Calculation Logic (Based on Telemetry)

Describe the metric in both natural language and formal definition.

- **Base Volume (e.g., TotalEntities)**:
	- Filter: <BASE_FILTERS_AND_TAGS>.
	- Calculation: <AGG_FUNCTION>(<COLUMN>) aggregated by <TIME_GRAIN>.
- **Subgroup Volume (e.g., TotalFailures / NeverSuccess)**:
	- Filter: <BASE_FILTERS> AND <ADDITIONAL_CONDITION>.
	- Calculation: <AGG_FUNCTION>(<COLUMN>) aggregated by <TIME_GRAIN>.

**Metric Formula**

- <METRIC_NAME> = (<NUMERATOR_EXPRESSION>) / (<DENOMINATOR_EXPRESSION>)
	- Example: <SUCCESS_RATE_METRIC> = (TotalEntities − TotalFailures) / TotalEntities.

#### 2.1.4. Targets, Thresholds, and Guardrails

- **Target Value**: <METRIC_NAME> >= <TARGET_VALUE>.
- **Volume Requirements**: Show base volume (e.g., TotalEntities) alongside the metric to confirm that trends are based on sufficient data.

#### 2.1.5. Recommended Breakdowns and Dimensions

By default, it could used any relevant columns which `IsAnalysisDimension` is tagged as `Yes` to slice the OKR for Corhort Analysis. If necessary, suggested analysis dimensions manually here. 

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
- Make time semantics explicit (e.g., calendar month vs rolling window).
- Clearly separate **global filters** (always on) from **ad-hoc filters** (used for explorations only).
- Keep this updated when new tables, measures, or OKRs are introduced so downstream tools and agents can reason accurately about telemetry.
- If any information cannot be gotten from PowerBI dashboard directly, highlight them and ask user to complete manually.

---



