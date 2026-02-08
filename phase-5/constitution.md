# Todo App Constitution - Phase V: Production Cloud Deployment

## Project Vision

Build a production-grade, event-driven, cloud-native application deployed on DigitalOcean Kubernetes with enterprise-level observability, resilience, and scalability. Demonstrate excellence in distributed systems architecture, event streaming with Apache Kafka, microservices communication with Dapr, and production operations with comprehensive monitoring and CI/CD automation.

**Phase V Goals:**
- Deploy to production cloud infrastructure (DigitalOcean Kubernetes)
- Implement event-driven architecture with Apache Kafka for asynchronous communication
- Use Dapr for distributed application runtime and service mesh capabilities
- Achieve production-grade observability with Prometheus, Grafana, and Jaeger
- Implement automated CI/CD pipeline with GitHub Actions
- Enable horizontal autoscaling and high availability
- Demonstrate cost optimization and operational excellence

## Core Principles

### I. Event-Driven Architecture (NON-NEGOTIABLE)

**All inter-service communication must be asynchronous and event-driven where appropriate.**

- Services communicate via events, not direct API calls (where applicable)
- Events are immutable facts about what happened
- Services are loosely coupled through event streams
- Event schemas are versioned and backward-compatible
- Event ordering is guaranteed within partitions
- Failed event processing is retried with exponential backoff
- Dead letter queues capture unprocessable events

**Event Categories**:
- **Domain Events**: Business-level events (TaskCreated, TaskCompleted, TaskDeleted)
- **Integration Events**: Cross-service communication events
- **System Events**: Infrastructure and operational events

**Rationale**: Event-driven architecture enables loose coupling, scalability, and resilience in distributed systems.

### II. Microservices with Dapr

**Dapr provides distributed application runtime capabilities.**

#### Dapr Building Blocks
- **Service Invocation**: Service-to-service calls with retries and circuit breakers
- **State Management**: Distributed state with Redis backend
- **Pub/Sub**: Event publishing and subscription via Kafka
- **Bindings**: Integration with external systems
- **Secrets Management**: Secure secret retrieval
- **Observability**: Distributed tracing with OpenTelemetry

#### Dapr Sidecar Pattern
- Every service has a Dapr sidecar container
- Sidecars handle cross-cutting concerns (retries, tracing, metrics)
- Application code uses Dapr SDK or HTTP/gRPC APIs
- Sidecars communicate via mTLS for security

#### Service Architecture
- **Backend API Service**: Existing FastAPI application (Phase 3)
- **Event Service**: New microservice for event processing
- **Frontend**: Next.js application (unchanged)
- **Database**: PostgreSQL (Neon or managed)

**Rationale**: Dapr simplifies microservices development by providing building blocks for common patterns.

### III. Production Cloud Infrastructure

**Infrastructure must be production-ready, scalable, and cost-optimized.**

#### DigitalOcean Kubernetes (DOKS)
- **Managed Kubernetes**: DigitalOcean handles control plane
- **Node Pools**: Separate pools for different workload types
- **Autoscaling**: Cluster autoscaler for node scaling
- **Load Balancer**: DigitalOcean Load Balancer for ingress
- **Container Registry**: DigitalOcean Container Registry (DOCR)

#### Infrastructure as Code
- **Terraform**: Provision DOKS cluster, node pools, load balancers
- **Version Control**: All infrastructure code in Git
- **State Management**: Terraform state in DigitalOcean Spaces or S3
- **Modular**: Reusable Terraform modules

#### High Availability
- **Multi-node Cluster**: 3+ nodes across availability zones
- **Pod Replicas**: 3+ replicas for critical services
- **Pod Disruption Budgets**: Ensure minimum availability during updates
- **Health Checks**: Comprehensive liveness and readiness probes
- **Graceful Shutdown**: Handle SIGTERM signals properly

**Rationale**: Production infrastructure must be reliable, scalable, and maintainable.

### IV. Observability and Monitoring

**System must be fully observable for debugging and optimization.**

#### Metrics (Prometheus)
- **Application Metrics**: Custom business metrics (tasks created, events processed)
- **System Metrics**: CPU, memory, disk, network
- **Kafka Metrics**: Lag, throughput, partition distribution
- **Dapr Metrics**: Service invocation latency, pub/sub metrics
- **Kubernetes Metrics**: Pod/node metrics, resource usage

#### Visualization (Grafana)
- **Pre-built Dashboards**: Kubernetes, Kafka, Dapr dashboards
- **Custom Dashboards**: Application-specific metrics
- **Alerting**: Alert rules for critical conditions
- **Annotations**: Mark deployments and incidents

#### Distributed Tracing (Jaeger)
- **End-to-End Tracing**: Track requests across services
- **Kafka Tracing**: Trace event publishing and consumption
- **Dapr Tracing**: Automatic tracing via Dapr sidecars
- **Performance Analysis**: Identify slow operations
- **Dependency Mapping**: Visualize service dependencies

#### Logging
- **Structured Logging**: JSON format for all services
- **Centralized**: Aggregate logs from all pods
- **Correlation IDs**: Track requests across services
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Retention**: Define retention policies

**Rationale**: Comprehensive observability enables rapid debugging, performance optimization, and proactive issue detection.

### V. Event Streaming with Kafka

**Kafka provides reliable, scalable event streaming.**

#### Kafka Architecture
- **Strimzi Operator**: Kubernetes-native Kafka deployment
- **Topics**: Separate topics for different event types
- **Partitions**: Multiple partitions for parallelism
- **Replication**: 3 replicas for fault tolerance
- **Retention**: Configurable retention policies

#### Event Design
- **Schema Registry**: Avro schemas for events
- **Versioning**: Backward-compatible schema evolution
- **Idempotency**: Events can be processed multiple times safely
- **Ordering**: Events ordered within partitions
- **Compaction**: Log compaction for state events

#### Event Topics
- `todo.tasks.created` - Task creation events
- `todo.tasks.updated` - Task update events
- `todo.tasks.deleted` - Task deletion events
- `todo.tasks.completed` - Task completion events
- `todo.analytics` - Analytics events

#### Consumer Groups
- **Event Service**: Processes all task events
- **Analytics Service**: Processes analytics events (future)
- **Notification Service**: Sends notifications (future)

**Rationale**: Kafka provides reliable, scalable event streaming for distributed systems.

### VI. CI/CD Automation

**Deployments must be automated, tested, and repeatable.**

#### GitHub Actions Pipeline
- **Build Stage**: Build Docker images, run tests
- **Push Stage**: Push images to DOCR with tags
- **Deploy Stage**: Deploy to DOKS using Helm
- **Test Stage**: Run smoke tests and integration tests
- **Notify Stage**: Send notifications on success/failure

#### Deployment Strategies
- **Staging**: Auto-deploy on merge to main branch
- **Production**: Manual approval required
- **Rollback**: Automatic rollback on health check failures
- **Blue-Green**: Optional blue-green deployments

#### Quality Gates
- **Tests**: All tests must pass before deployment
- **Security Scanning**: Scan images for vulnerabilities
- **Linting**: Helm chart linting
- **Smoke Tests**: Basic health checks after deployment

**Rationale**: Automated CI/CD enables rapid, reliable deployments with quality assurance.

### VII. Cost Optimization

**Cloud resources must be used efficiently to minimize costs.**

#### Resource Optimization
- **Right-sizing**: Use appropriate node sizes (s-2vcpu-4gb initially)
- **Autoscaling**: Scale down during low traffic periods
- **Spot Instances**: Use spot instances for non-critical workloads (if available)
- **Resource Limits**: Prevent resource waste with proper limits
- **Cluster Autoscaler**: Scale nodes based on demand

#### Database Strategy
- **Neon Serverless**: Pay-per-use PostgreSQL (cheaper than managed)
- **Connection Pooling**: Minimize database connections
- **Query Optimization**: Efficient queries with indexes

#### Monitoring Costs
- **Metrics Retention**: Limit Prometheus retention (7-14 days)
- **Log Retention**: Limit log retention (7 days)
- **Sampling**: Sample traces (not 100% tracing)

#### Cleanup Strategy
- **Development Clusters**: Destroy when not in use
- **Unused Resources**: Regular cleanup of unused PVCs, images
- **Cost Monitoring**: Track spending with DigitalOcean dashboard

**Rationale**: Cloud costs can escalate quickly. Optimization is essential for sustainability.

### VIII. Security Best Practices

**Production systems require defense-in-depth security.**

#### Network Security
- **Network Policies**: Restrict pod-to-pod communication
- **Ingress TLS**: HTTPS for all external traffic
- **Service Mesh**: mTLS between services (via Dapr)
- **Private Networking**: Use DigitalOcean VPC

#### Secrets Management
- **Kubernetes Secrets**: Encrypted at rest
- **External Secrets**: Consider External Secrets Operator
- **Rotation**: Regular secret rotation
- **Least Privilege**: Minimal permissions for service accounts

#### Container Security
- **Non-root Users**: All containers run as non-root
- **Image Scanning**: Scan for vulnerabilities in CI/CD
- **Minimal Images**: Use Alpine or distroless base images
- **Security Context**: Define security context for all pods

#### RBAC
- **Service Accounts**: Dedicated service accounts per service
- **Roles**: Fine-grained roles and role bindings
- **Audit Logging**: Enable Kubernetes audit logs

**Rationale**: Security breaches can be catastrophic. Multiple layers of defense are essential.

### IX. Operational Excellence

**Operations must be efficient, automated, and well-documented.**

#### Runbooks
- **Deployment Runbook**: Step-by-step deployment guide
- **Incident Response**: Procedures for common incidents
- **Rollback Procedures**: How to rollback deployments
- **Disaster Recovery**: Backup and restore procedures

#### Monitoring and Alerting
- **SLIs/SLOs**: Define service level indicators and objectives
- **Alert Rules**: Alert on SLO violations
- **On-Call**: Define on-call rotation (if applicable)
- **Escalation**: Define escalation procedures

#### Documentation
- **Architecture Diagrams**: Visual representation of system
- **API Documentation**: OpenAPI/Swagger for all APIs
- **Event Schemas**: Document all event types
- **Troubleshooting Guide**: Common issues and solutions

**Rationale**: Operational excellence reduces downtime and improves team efficiency.

### X. Resilience and Fault Tolerance

**System must gracefully handle failures.**

#### Retry Strategies
- **Exponential Backoff**: Retry failed operations with increasing delays
- **Circuit Breakers**: Prevent cascading failures (via Dapr)
- **Timeouts**: Set appropriate timeouts for all operations
- **Idempotency**: Operations can be retried safely

#### Data Consistency
- **Event Sourcing**: Events as source of truth
- **Eventual Consistency**: Accept eventual consistency where appropriate
- **Compensating Transactions**: Handle failures with compensations
- **Saga Pattern**: Coordinate distributed transactions

#### Failure Scenarios
- **Pod Failures**: Kubernetes restarts failed pods
- **Node Failures**: Pods rescheduled to healthy nodes
- **Kafka Failures**: Replication ensures no data loss
- **Database Failures**: Connection pooling and retries

**Rationale**: Distributed systems fail. Resilience must be built-in.

## Technology Stack

### Cloud Infrastructure
- **Kubernetes**: DigitalOcean Kubernetes (DOKS) 1.28+
- **Container Registry**: DigitalOcean Container Registry (DOCR)
- **Load Balancer**: DigitalOcean Load Balancer
- **VPC**: DigitalOcean Virtual Private Cloud
- **IaC**: Terraform 1.6+ or doctl CLI

### Event Streaming
- **Apache Kafka**: 3.6+ via Strimzi Operator 0.38+
- **Schema Registry**: Confluent Schema Registry or Apicurio
- **Kafka UI**: Kafka UI for management (optional)

### Distributed Runtime
- **Dapr**: 1.12+ for distributed application runtime
- **Dapr Components**: Kafka pub/sub, Redis state store
- **Dapr SDK**: Python SDK for backend, JavaScript SDK for frontend

### Monitoring Stack
- **Prometheus**: 2.48+ for metrics collection
- **Grafana**: 10.2+ for visualization
- **Jaeger**: 1.51+ for distributed tracing
- **Alertmanager**: For alert routing

### CI/CD
- **GitHub Actions**: Workflow automation
- **Docker**: Image building
- **Helm**: Deployment management

### Existing Stack (Phase 3-4)
- **Backend**: FastAPI, SQLModel, PostgreSQL, OpenAI Agents SDK
- **Frontend**: Next.js, React, TypeScript, OpenAI ChatKit
- **Database**: PostgreSQL (Neon Serverless)

## Non-Negotiable Constraints

### Technical Constraints
1. **Cloud Deployment**: Must deploy to DigitalOcean Kubernetes (DOKS)
2. **Event-Driven**: Must use Apache Kafka for event streaming
3. **Dapr Required**: Must use Dapr for service communication
4. **Production-Grade**: High availability, monitoring, autoscaling
5. **CI/CD**: Automated deployment pipeline
6. **Observability**: Prometheus, Grafana, Jaeger required
7. **Cost-Conscious**: Optimize for cost efficiency

### Development Constraints
1. **Specification First**: No implementation without specifications
2. **Infrastructure as Code**: All infrastructure in Terraform or scripts
3. **Automated Testing**: Tests in CI/CD pipeline
4. **Documentation**: Comprehensive deployment and operational guides
5. **Security**: Follow security best practices

### Operational Constraints
1. **High Availability**: 3+ replicas for critical services
2. **Monitoring**: All services instrumented
3. **Alerting**: Critical alerts configured
4. **Backup**: Database backup strategy
5. **Disaster Recovery**: Documented recovery procedures

## Success Metrics

Phase V is successful when:

1. Application deployed to DOKS and accessible via public URL
2. Kafka cluster running with 3 brokers
3. Dapr sidecars injected into all services
4. Events flowing through Kafka (create task → event published → consumed)
5. Distributed tracing working (traces visible in Jaeger)
6. Metrics collected (visible in Grafana dashboards)
7. Autoscaling working (HPA scales pods based on load)
8. CI/CD pipeline deploying automatically
9. All Phase 3 functionality working in production
10. System handles failures gracefully
11. Cost optimized (< $100/month for demo)
12. Documentation complete

## Project Constraints Summary

**DO:**
- Write specifications before implementation
- Use event-driven patterns for async operations
- Implement Dapr for service communication
- Deploy to real cloud (DOKS)
- Set up comprehensive monitoring
- Automate with CI/CD
- Optimize for cost
- Document everything
- Test thoroughly
- Plan for failures

**DON'T:**
- Skip event-driven architecture
- Use synchronous calls where async is appropriate
- Deploy without monitoring
- Ignore cost optimization
- Skip security best practices
- Deploy without testing
- Leave cluster running when not needed
- Ignore alerts and metrics
- Over-provision resources
- Skip documentation

---

**Version**: 5.0.0
**Ratified**: 2026-02-04
**Last Amended**: 2026-02-04
**Next Review**: After Phase V completion
**Supersedes**: Constitution v4.0.0 (Phase IV)
**Extends**: Production cloud and event-driven architecture principles
