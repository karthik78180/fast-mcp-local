# PRB-2024-002: Memory Leak in Kubernetes Pod

## Incident Summary
- **PRB ID**: PRB-2024-002
- **Date**: 2024-02-03
- **Severity**: High
- **Status**: Resolved
- **Affected Systems**: Payment Service (Kubernetes pods)
- **Impact**: Intermittent payment processing delays, 15% of requests affected
- **Duration**: 6 hours (detection to full resolution)

## Timeline
- 08:00 - Deployed payment-service v2.5.0 to production
- 10:30 - First customer complaints about slow payment processing
- 11:00 - CloudWatch alarm: payment-service pod memory usage > 90%
- 11:15 - SRE investigated memory metrics, observed gradual increase
- 11:30 - Identified memory leak pattern in heap dump
- 12:00 - Rollback initiated to v2.4.0
- 12:15 - Rollback completed, memory usage stabilized
- 14:00 - Root cause identified in code: unclosed HTTP client connections
- 14:00 - Fix developed and tested

## Root Cause Analysis
Memory leak was caused by HTTP client connections not being properly closed in the new payment gateway integration code.

### Primary Cause
In `PaymentGatewayClient.java`, HTTP client connections were created but never closed:

```java
// Bug: Connection never closed
HttpClient client = HttpClient.newHttpClient();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
return response.body();
```

Each payment request created a new HTTP client and connection, consuming memory. After ~1000 requests, pod memory reached limit and Kubernetes killed the pod.

### Contributing Factors
- New HTTP client library (migrated from RestTemplate to HttpClient)
- Code review didn't catch the resource leak
- Insufficient load testing (tested with only 100 requests)
- Memory leak detection tools not run in CI/CD

### Why It Happened
- Developer unfamiliar with HttpClient resource management
- No automated memory leak detection in pre-production
- Load testing duration too short to detect slow leaks

## Resolution
### Immediate Actions
1. Rolled back to previous stable version (v2.4.0)
2. Scaled up pod replicas to handle load during investigation
3. Communicated issue to payment gateway team

### Permanent Fix
Fixed resource management in `PaymentGatewayClient.java`:

```java
// Fixed: Reuse single HttpClient instance
private static final HttpClient client = HttpClient.newHttpClient();

public String makeRequest(HttpRequest request) throws Exception {
    HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
    return response.body();
}
```

### Verification
- Ran 10,000 requests in staging: memory usage remained stable
- Monitored production for 24 hours post-deployment: no memory growth
- Heap dump analysis showed no retained HTTP client objects

## Action Items
- [x] Rollback to v2.4.0 (Owner: @sre-team, Due: 2024-02-03) - COMPLETED
- [x] Fix resource leak in code (Owner: @payment-team, Due: 2024-02-03) - COMPLETED
- [x] Deploy fixed version v2.5.1 (Owner: @payment-team, Due: 2024-02-04) - COMPLETED
- [ ] Add memory leak detection to CI/CD (Owner: @platform-team, Due: 2024-02-15)
- [ ] Extend load test duration to 1 hour minimum (Owner: @qa-team, Due: 2024-02-15)
- [ ] Create HTTP client usage guidelines (Owner: @backend-team, Due: 2024-02-20)
- [ ] Add memory growth alerting for all services (Owner: @sre-team, Due: 2024-02-20)
- [ ] Conduct training on resource management best practices (Owner: @backend-team, Due: 2024-03-01)

## Prevention
### Short-term Measures
- Added automated memory leak detection using Java Flight Recorder in CI/CD
- Implemented pod memory growth alerts (>10% increase per hour)
- Created resource management code review checklist

### Long-term Improvements
- Establish performance testing standards (minimum 1 hour load test)
- Implement automatic heap dump collection on OOM events
- Create resource management patterns documentation
- Add static analysis for resource leaks (SpotBugs, ErrorProne)

## Lessons Learned
### What Went Well
- Fast rollback decision (30 minutes from identification)
- Good collaboration between SRE and payment teams
- Heap dump analysis quickly identified root cause

### What Could Be Improved
- Load testing duration was insufficient
- Memory leak detection should be automated
- Better developer education on resource management
- Earlier customer impact detection (complaints came before alerts)

### What We Got Lucky With
- Issue manifested during business hours
- Low-severity impact (only 15% of requests affected)
- Simple rollback path available

## Impact Analysis
### Customer Impact
- **Affected Payments**: ~450 payments experienced delays (15% of volume during incident)
- **Average Delay**: 5-10 seconds additional processing time
- **Failed Payments**: 0 (all eventually processed)
- **Customer Complaints**: 12 support tickets filed

### Business Impact
- **Revenue Impact**: None (all payments completed)
- **SLA Breach**: No (response time SLA: <2s, actual: <12s during incident)
- **Reputation Impact**: Minor (resolved quickly, proactive communication)

## Communication Log
- 11:00 - Created incident Slack channel (#inc-payment-memory-leak)
- 11:30 - Posted update: "Investigating memory leak in payment service"
- 12:00 - Posted update: "Rolling back to stable version"
- 12:30 - Posted update: "Rollback complete, monitoring stability"
- 14:30 - Posted update: "Root cause identified, fix in progress"
- Next day - Posted postmortem in #engineering-all

## Monitoring & Alerts
### New Alerts Added
- Pod memory usage growth rate > 10% per hour
- Pod memory usage > 85% (warning), > 95% (critical)
- OOM kill events in Kubernetes

### New Dashboards
- Service memory usage trends (24h, 7d, 30d views)
- JVM heap metrics per service
- HTTP client connection pool metrics

---
**Created**: 2024-02-03
**Last Updated**: 2024-02-04
**Owner**: SRE Team
**Postmortem Meeting**: 2024-02-05 @ 10:00 AM
**Attendees**: SRE Team, Payment Team, Backend Team Lead
