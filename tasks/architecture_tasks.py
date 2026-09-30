"""
Architecture Task

Generates software architecture from software requirements.
"""

from crewai import Task


def create_architecture_task(agent, requirements: str):
    """
    Creates the Architecture Task for the Solution Architect agent.
    Enforces the systematic 15-step System Design Workflow Reference.
    """

    description = f"""
You are the Principal Solution Architect. Your task is to design a robust, scalable,
and production-ready system architecture based on the provided requirements.

Follow the systematic System Design Workflow:

1. Executive Summary & Problem Framing (context, business goals, scope boundaries)
2. Functional Capabilities & Core User Journeys
3. Non-Functional Requirements & SLOs (Availability, p95 Latency, Throughput, Scalability, Consistency)
4. Scale & Capacity Estimation (traffic profile, storage growth, cache & DB sizing)
5. High-Level Architecture (system context, component boundaries, sync vs async communications)
6. Mermaid Architecture Diagram (clear component and request flow diagram)
7. Data Modeling & Storage Strategy (relational entities, caching layer, retention policies)
8. API Design & Contracts (key REST endpoints, request/response models, idempotency)
9. Reliability & Resilience (failover, circuit breakers, retry policies with jitter, rate limiting)
10. Security & Compliance Architecture (authentication, authorization, encryption, trust boundaries)
11. Observability & Operational Plan (metrics, structured logging, distributed tracing, alerts)
12. Trade-off Analysis & Architectural Decision Log (ADRs, rationale for chosen vs rejected alternatives)

Requirements:
{requirements}

Return the response strictly as a structured Markdown document using clear headings, tables, and Mermaid diagrams.
"""

    expected_output = (
        "A comprehensive, production-grade Software Architecture Document in Markdown "
        "conforming to the 15-step System Design Workflow Reference, including Mermaid diagrams, "
        "capacity models, data schemas, API contracts, resilience patterns, and explicit trade-off analyses."
    )

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
    )