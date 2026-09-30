# System Design Workflow Reference

This document is a practical workflow for designing scalable, reliable, and maintainable systems. It can be used for architecture reviews, technical planning, or system-design interviews.

## 1. Frame the Problem

Start by clarifying the business and technical context before proposing a design.

### Questions to answer
- What problem are we solving?
- Who are the users and what are their expectations?
- What are the critical user journeys?
- What does success look like in terms of latency, throughput, availability, and cost?
- What are the functional and non-functional requirements?

### Output
- Problem statement
- Scope definition (in scope vs out of scope)
- Key constraints and assumptions

---

## 2. Define Functional Requirements

Break the problem into domain capabilities and user actions.

### Example
For a ride-sharing platform:
- User creates account
- Search for nearby drivers
- Book ride
- Track driver location
- Make payment
- Rate trip

### Output
- User stories or use cases
- API operations and workflow steps
- Data entities required by the application

---

## 3. Define Non-Functional Requirements

This is where architecture decisions start to become concrete.

### Typical NFRs
- Availability: 99.9%
- Latency: p95 under 300 ms
- Throughput: requests per second or transactions per minute
- Scalability: support future growth by 10x or 100x
- Consistency: strong vs eventual consistency
- Security: authentication, authorization, encryption, auditing
- Cost: cloud budget or infra constraints
- Observability: logging, metrics, tracing

### Output
- Target SLAs and SLOs
- Capacity assumptions
- Reliability goals

---

## 4. Estimate Scale and Capacity

Use rough numbers to shape the architecture.

### Common estimation inputs
- Daily or monthly active users
- Read/write ratio
- Peak requests per second
- Average request size
- Data retention requirements
- Storage growth assumptions

### Example formulas
- Requests per second = daily traffic / 86400 × peak factor
- Storage = row size × total rows × retention period
- Bandwidth = payload size × request rate

### Output
- Expected traffic profile
- Storage estimate
- Cache and database sizing assumptions
- Scaling requirements for each component

---

## 5. Design the High-Level Architecture

Choose a high-level structure that satisfies the requirements without over-engineering.

### Common patterns
- Monolith first for simpler systems
- Microservices for independent scaling and team ownership
- Event-driven architecture for async workflows
- CQRS and read models for heavy read workloads
- Layered architecture for separation of concerns

### Design decisions to capture
- Clients and access channels
- Internal services and responsibilities
- Communication model (sync vs async)
- Data flow between components
- Domain boundaries and ownership

### Output
- System context diagram
- Component diagram
- Service boundaries
- Request flow

---

## 6. Define Data Model and Storage Strategy

Select the right storage solution for each data type.

### Considerations
- Transactional data: relational DB
- High-volume logs/events: object store or append log
- Search and analytics: search index or analytical warehouse
- Caching: Redis or in-memory cache
- Streaming: Kafka, Pub/Sub, or similar

### Questions to answer
- What data is relational?
- What requires high write throughput?
- What requires low-latency reads?
- How often does data change?
- What needs eventual consistency?

### Output
- Entity definitions
- Relationships and indexes
- Storage technology selection per data domain
- Backup and retention strategy

---

## 7. Define APIs and Contracts

Create clear interfaces before implementation.

### API design checklist
- Use REST or gRPC based on system needs
- Define request/response schemas
- Specify error codes and retry semantics
- Document rate limits and auth expectations
- Define idempotency for write operations

### Output
- API contract document
- Endpoints and payloads
- Authentication and authorization model
- Backoff/retry behavior

---

## 8. Design for Reliability and Resilience

Reliability is not an afterthought; it belongs in the initial architecture.

### Key mechanisms
- Load balancing
- Caching
- Rate limiting
- Retry with jitter
- Circuit breakers
- Timeouts
- Bulkheads
- Queue-based decoupling
- Replication and failover
- Health checks and auto-recovery

### Output
- Failure mode analysis
- Resilience strategy
- Recovery plan for degraded systems

---

## 9. Design for Security and Compliance

Protect identity, data, and system boundaries.

### Security checklist
- Authentication and authorization
- Role-based or attribute-based access control
- Secret management
- Encryption in transit and at rest
- Data privacy and retention rules
- Audit logging
- Input validation and sanitization
- Dependency and vulnerability scanning

### Output
- Security architecture
- Trust boundaries
- Compliance considerations
- Risk register

---

## 10. Plan for Observability and Operations

A system is only manageable if operators can reason about it.

### Include
- Structured logs
- Metrics and dashboards
- Distributed tracing
- Alerting and on-call procedures
- Runbooks
- Deployment strategy
- Environment config management

### Output
- Monitoring plan
- Alert thresholds
- Operational ownership model

---

## 11. Validate the Design Against Requirements

Before finalizing, test the design against the business and technical goals.

### Validation checklist
- Does it satisfy the traffic and latency goals?
- Does it fail gracefully under overload?
- Does the data model support growth?
- Are the security boundaries correct?
- Can the system be operated and debugged by a team?
- Is the design cost-effective?

### Output
- Review notes
- Trade-off list
- Risks and mitigations

---

## 12. Make Trade-Offs Explicit

A strong design does not avoid trade-offs; it makes them visible and justified.

### Common trade-offs
- Consistency vs availability
- Latency vs cost
- Simplicity vs flexibility
- Strong coupling vs loose coupling
- Batch processing vs real-time processing

### Output
- Decision log
- Why alternative options were rejected
- Open questions and next steps

---

## 13. Final Deliverable Template

A reference architecture review should end with a concise, structured summary.

### Suggested structure
1. Problem statement
2. Requirements summary
3. Assumptions and constraints
4. High-level architecture
5. Component responsibilities
6. Data model and storage
7. API and interface design
8. Reliability and security design
9. Scaling and performance plan
10. Observability and operations
11. Risks, trade-offs, and open questions

---

## 14. Example Workflow for a Real System

### Example: Social Media Feed Service

1. Clarify requirements
   - Users create posts
   - Feed is personalized
   - Access latency target is < 200 ms p95
   - Home feed needs high read throughput

2. Estimate scale
   - 100M MAU
   - 3 posts/user/day
   - 10x peak traffic during launches

3. High-level design
   - Web/mobile clients
   - API gateway
   - Feed service
   - Post service
   - User graph service
   - Cache layer
   - Storage for posts and social graph

4. Data model
   - Relational DB for users and posts
   - Redis for hot feed cache
   - Search index for discovery features

5. Reliability
   - Queue for asynchronous fan-out
   - Retries and rate limits
   - Read replicas for feed queries

6. Observability
   - Metrics for feed latency, cache hit ratio, write lag
   - Alerts when ingestion backlog exceeds threshold

7. Trade-offs
   - Prefer denormalized feed materialization for scale
   - Accept eventual consistency for feed updates

---

## 15. Practical Checklist

Use this checklist before finalizing any system design.

- Requirements are clear and complete
- Traffic and data estimates are documented
- Core use cases are mapped to services
- Data model and storage decisions are justified
- Reliability and failover patterns are included
- Security model is defined
- Scaling strategy is explained
- Monitoring and alerting are planned
- Trade-offs are documented

This workflow is intentionally iterative: start broad, validate assumptions, and refine architecture as constraints become clearer.
