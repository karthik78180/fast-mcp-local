# PRB-2024-001: Database Connection Pool Exhaustion

## Incident Summary
- **PRB ID**: PRB-2024-001
- **Date**: 2024-01-15
- **Severity**: Critical
- **Status**: Resolved
- **Affected Systems**: API Gateway, Backend Service, PostgreSQL Database
- **Impact**: 100% of API requests failing with 503 errors
- **Duration**: 45 minutes

## Timeline
- 14:30 - PagerDuty alert: API Gateway 5xx error rate spike
- 14:32 - SRE on-call acknowledged incident
- 14:35 - Confirmed database connection pool exhausted (all 100 connections in use)
- 14:40 - Identified slow queries holding connections open
- 14:45 - Killed long-running queries, connections released
- 14:50 - API Gateway health restored, error rate returned to normal
- 15:15 - All services verified healthy

## Root Cause Analysis
The database connection pool was exhausted due to a combination of:

1. **Primary Cause**: A new API endpoint deployed at 14:00 that executed an unoptimized query with missing index
2. **Contributing Factor**: Connection pool size (100) was too small for peak load
3. **Contributing Factor**: No query timeout configured, allowing connections to be held indefinitely

### Why It Happened
- Code review didn't catch the missing database index
- Load testing didn't include this new endpoint
- Database connection monitoring alerts were not in place

## Resolution
### Immediate Actions
1. Identified and killed slow queries using `pg_stat_activity`
2. Released database connections back to pool
3. Disabled the problematic API endpoint temporarily

### Permanent Fix
1. Added missing index on `users.created_at` column
2. Increased connection pool size from 100 to 200
3. Added 30-second query timeout configuration

## Action Items
- [x] Add missing database index (Owner: @db-team, Due: 2024-01-15) - COMPLETED
- [x] Increase connection pool size (Owner: @sre-team, Due: 2024-01-15) - COMPLETED
- [x] Add query timeout configuration (Owner: @backend-team, Due: 2024-01-16) - COMPLETED
- [ ] Implement database connection pool monitoring (Owner: @sre-team, Due: 2024-01-22)
- [ ] Add slow query alerting (Owner: @db-team, Due: 2024-01-22)
- [ ] Update code review checklist to include index review (Owner: @backend-team, Due: 2024-01-25)
- [ ] Add load testing for new endpoints to CI/CD (Owner: @platform-team, Due: 2024-02-01)

## Prevention
### Short-term Measures
- Added CloudWatch alarms for database connection pool utilization
- Implemented query timeout across all services
- Created runbook for connection pool exhaustion incidents

### Long-term Improvements
- Implement automatic slow query detection in CI/CD
- Migrate to connection pooler (PgBouncer) for better connection management
- Establish database performance review as part of deployment process

## Lessons Learned
### What Went Well
- Fast detection via PagerDuty alert (2 minutes from incident start)
- Quick identification of root cause using pg_stat_activity
- Effective communication with stakeholders via Slack incident channel

### What Could Be Improved
- Load testing should have caught this before production
- Missing index should have been caught in code review
- Database monitoring was insufficient (no connection pool alerts)

## Communication Log
- 14:32 - Posted incident channel in Slack
- 14:40 - Updated status page: "Investigating API errors"
- 14:50 - Updated status page: "Issue resolved, monitoring"
- 15:15 - Posted all-clear in incident channel
- 15:30 - Sent incident summary email to engineering team

## Monitoring & Alerts
### New Alerts Added
- Database connection pool utilization > 80%
- Query execution time > 10 seconds
- Database connection wait time > 5 seconds

### Dashboard Updates
- Added connection pool metrics to main SRE dashboard
- Created database performance dashboard

---
**Created**: 2024-01-15
**Last Updated**: 2024-01-16
**Owner**: SRE Team
**Post-Incident Review**: 2024-01-17 @ 2:00 PM
