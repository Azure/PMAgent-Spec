# M365 Agents Toolkit — Status Report (Release 6.5)

## Executive Summary

**Overall Health: Yellow**

The M365 Agents Toolkit 6.5 release is progressing with 6 active features, 2 closed user stories, and 3 open bugs. Key achievements include completion of the App Manifest version check feature and CEA Basic Template for Python SDK. Critical challenges include 3 new bugs requiring resolution and delayed work on Conditional Access policies support. The release contains partner-driven features scheduled for post-Ignite delivery, with active development underway.

## Feature Progress Overview

| Feature | Owner | Progress % | Status | Notes |
|---------|-------|-----------|--------|-------|
| App Manifest version check | Ning Tang | 88% | On Track | 7/8 child items completed |
| Support Conditional Access policies for ATK login | Huihui Wu | 14% | At Risk | 1/7 stories completed, post-Ignite timeline |
| Support configuration + template | Ning Tang | 0% | At Risk | 0/1 stories completed, in Active state |
| CEA python template using Agents SDK | Ning Tang | 100% | Completed | Template delivered |
| Make Travel Agent sample into C# template | Qinzhou Xu | 0% | Active | Recently started, post-Ignite delivery |
| Support Importing Templates | Unassigned | 0% | Not Started | Planning phase |
| Support environment management | Unassigned | 0% | Not Started | Planning phase |

## Completion Metrics

- **Total Work Items**: 12 (6 Features, 2 User Stories, 1 Bug, 3 Bugs)
- **Completed Items**: 2 User Stories (100% completion), 7/8 tasks for App Manifest feature
- **Active Items**: 6 Features, 2 User Stories in Active state
- **Features Completion Rate**: 17% (1/6 active features fully completed)
- **Overall Progress**: ~35% of planned work for 6.5 release completed

## Dependency Status

| Dependency | Owner | Status | Risk Level | Notes |
|------------|-------|--------|-----------|-------|
| MSAL Authentication Broker | Huihui Wu | In Progress | Medium | Required for Conditional Access policies feature |
| App Manifest Schema 1.24 | Ning Tang | Completed | Low | Successfully updated and closed |
| Teams AI Alignment | Ning Tang | Pending | Medium | Configuration + template work depends on Teams AI team alignment |
| Partner Feedback (Travel Agent) | Qinzhou Xu | In Progress | Low | Template development in progress |

## Bug / Issue Summary

| Severity | Active | Resolved | Closed | Total |
|----------|--------|----------|--------|-------|
| High | 0 | 0 | 0 | 0 |
| Medium | 0 | 0 | 0 | 0 |
| Low | 0 | 0 | 0 | 0 |
| Unspecified | 3 | 0 | 0 | 3 |

### Bug Trend Analysis

Three new bugs have been identified for the 6.5 release, all currently in "New" state:

### Key Bugs

| Bug ID | Title | Severity | Status | Owner | Priority |
|--------|-------|----------|--------|-------|----------|
| 35858710 | The image in the Copilot connector template readme file is not updated | Unspecified | New | Yu Zhang | QA Issue |
| 35869528 | DA + action from spec will write data endlessly | Unspecified | New | Zhiyu You | Critical |
| 35799759 | Update old aka.ms URL in our UI hovering message | Unspecified | New | Yu Zhang | Low |

**Trend**: All three bugs were filed in November 2025, indicating recent testing activity. The infinite data write bug (35869528) requires immediate attention as it impacts core functionality.

## Risks & Blockers

1. **Critical Bug - Infinite Data Write (35869528)**
   - **Impact**: High - Core declarative agent + action functionality affected
   - **Mitigation**: Assign priority investigation and fix

2. **Conditional Access Policies Feature Delay**
   - **Impact**: High - Security compliance requirement for MS tenant users
   - **Mitigation**: 1/7 stories completed; requires acceleration or timeline adjustment post-Ignite

3. **Unassigned Features**
   - **Impact**: Medium - Two features (Import Templates, Environment Management) lack ownership
   - **Mitigation**: Assign owners and clarify priorities for 6.5 scope

4. **Partner Ask Dependencies**
   - **Impact**: Medium - Multiple features tagged "PartnerAsk" and "post-Ignite"
   - **Mitigation**: Confirm post-Ignite delivery timeline aligns with partner expectations

5. **Testing Coverage**
   - **Impact**: Medium - QA tag on bug 35858710 suggests testing has begun; additional issues may surface
   - **Mitigation**: Continue QA cycle and prioritize bug fixes

## Engineering Health

**Build & Test Status**: Data not available

**Code Quality Indicators**:
- 2 User Stories successfully closed (CEA Basic Template, App Manifest updates)
- Multiple app manifest version updates completed (1.21 → 1.24 progression)

**Known Issues**:
- Infinite write loop in DA + action from spec (Bug 35869528)
- Documentation/template quality issues (outdated images, URLs)

## Forecast & Next Steps

**Expected Timeline**:
- **Post-Ignite (Late November 2025)**: Delivery of partner-driven features (Travel Agent template, Configuration + template support)
- **December 2025**: Complete Conditional Access policies support
- **Release Target**: Early Q1 2026 (pending bug resolution and feature completion)

**Immediate Priorities**:
1. **Fix critical bug 35869528** - DA + action infinite write issue
2. **Accelerate Conditional Access feature** - Complete remaining 6/7 user stories
3. **Assign owners to unassigned features** - Import Templates and Environment Management
4. **Complete QA cycle** - Address remaining documentation and UI bugs
5. **Partner alignment** - Confirm post-Ignite delivery schedule for partner-dependent features

**Next Iteration Focus**:
- Close all New bugs (target: 100% resolution)
- Complete App Manifest feature (1 remaining task)
- Progress Conditional Access to 50%+ completion
- Begin work on unassigned features or descope from 6.5

## Appendix

### Work Item Summary by Type

**Features (6)**:
- 33501925: App Manifest version check (Active, 88%)
- 33871096: Support Conditional Access policies (Active, 14%)
- 35069693: Support configuration + template (Active, 0%)
- 34517948: CEA python template (Active, related to vsc 6.5.1)
- 35948060: Travel Agent C# template (Active, 0%)
- 35069794: Support Importing Templates (New, 0%)
- 35069931: Support environment management (New, 0%)

**User Stories (2)**:
- 35915935: Add CEA Basic Template for Python SDK (Closed) ✓
- 35917723: Enable dynamic template release including UI changes (Active)

**Bugs (3)**:
- 35858710: Copilot connector template readme image not updated (New)
- 35869528: DA + action from spec writes data endlessly (New) 
- 35799759: Update old aka.ms URL in UI hovering message (New)

### Additional Context

- **Release Tag**: VSC 6.5 (Visual Studio Code extension version 6.5)
- **Related Tags**: H2CY2025, post-Ignite, PartnerAsk
- **Project**: Microsoft Teams Extensibility
- **Report Date**: November 25, 2025
