import { useState } from "react";

const layers = [
  {
    id: "users",
    label: "USER LAYER",
    color: "#0EA5E9",
    glow: "rgba(14,165,233,0.35)",
    nodes: [
      { id: "patient", icon: "🧑‍⚕️", label: "Patient Portal", sub: "Next.js" },
      { id: "physician", icon: "👨‍⚕️", label: "Physician Dashboard", sub: "React + TypeScript" },
      { id: "staff", icon: "🏥", label: "Staff Interface", sub: "React + TypeScript" },
      { id: "admin", icon: "⚙️", label: "Admin Console", sub: "React + TypeScript" },
    ],
  },
  {
    id: "gateway",
    label: "SECURITY & GATEWAY LAYER",
    color: "#F59E0B",
    glow: "rgba(245,158,11,0.35)",
    nodes: [
      { id: "apigw", icon: "🔀", label: "API Gateway", sub: "AWS API Gateway / Kong" },
      { id: "auth", icon: "🔐", label: "Identity & Auth", sub: "AWS Cognito + Auth0 (RBAC)" },
      { id: "waf", icon: "🛡️", label: "WAF + Firewall", sub: "AWS WAF + Shield" },
      { id: "audit", icon: "📋", label: "Audit Trail", sub: "AWS CloudTrail" },
    ],
  },
  {
    id: "api",
    label: "APPLICATION LAYER",
    color: "#8B5CF6",
    glow: "rgba(139,92,246,0.35)",
    nodes: [
      { id: "fastapi", icon: "⚡", label: "FastAPI Backend", sub: "Python · REST + WebSockets" },
      { id: "celery", icon: "⏱️", label: "Task Queue", sub: "Celery + Redis" },
      { id: "fhir", icon: "🔗", label: "FHIR R4 Engine", sub: "HL7 Interoperability" },
      { id: "ws", icon: "💬", label: "Real-time Messaging", sub: "WebSocket · Encrypted" },
    ],
  },
  {
    id: "ai",
    label: "AI & ML LAYER",
    color: "#10B981",
    glow: "rgba(16,185,129,0.35)",
    nodes: [
      { id: "claude", icon: "🤖", label: "Claude API", sub: "Clinical Notes · Triage · Coding" },
      { id: "stt", icon: "🎙️", label: "Speech-to-Text", sub: "AWS Transcribe Medical" },
      { id: "nlp", icon: "🧠", label: "NLP Pipeline", sub: "ICD-10 · CPT Extraction" },
      { id: "validation", icon: "✅", label: "AI Validator", sub: "Hallucination Guard · Review Gate" },
    ],
  },
  {
    id: "data",
    label: "DATA LAYER",
    color: "#EF4444",
    glow: "rgba(239,68,68,0.35)",
    nodes: [
      { id: "postgres", icon: "🗄️", label: "PostgreSQL (RDS)", sub: "Primary · HIPAA Encrypted" },
      { id: "replica", icon: "📊", label: "Analytics Replica", sub: "Read-only · Metabase" },
      { id: "s3", icon: "🗃️", label: "Document Store", sub: "AWS S3 · AES-256" },
      { id: "kms", icon: "🔑", label: "Key Management", sub: "AWS KMS · Field Encryption" },
    ],
  },
  {
    id: "integrations",
    label: "EXTERNAL INTEGRATIONS",
    color: "#EC4899",
    glow: "rgba(236,72,153,0.35)",
    nodes: [
      { id: "lab", icon: "🧪", label: "Lab Systems", sub: "HL7 v2 · FHIR Results" },
      { id: "pharmacy", icon: "💊", label: "Pharmacy / eRx", sub: "Surescripts · DEA Compliant" },
      { id: "insurance", icon: "📄", label: "Insurance / Payers", sub: "Availity · Change Healthcare" },
      { id: "comms", icon: "📱", label: "Patient Comms", sub: "Twilio SMS · SendGrid" },
    ],
  },
];

const detailMap = {
  patient: { title: "Patient Portal", desc: "Secure scheduling, messaging, lab results, prescription refills, AI health assistant with plain-language explanations. 15-min session timeout (HIPAA)." },
  physician: { title: "Physician Dashboard", desc: "Ambient documentation, SOAP note generation, clinical decision support, AI-suggested ICD-10/CPT codes, encounter timeline." },
  staff: { title: "Staff Interface", desc: "HIPAA-compliant internal messaging, smart routing, shift handoff summaries, alert escalation to on-call providers." },
  admin: { title: "Admin Console", desc: "User management, RBAC configuration, system health, compliance reporting, AI performance metrics." },
  apigw: { title: "API Gateway", desc: "Single security perimeter for all traffic. Rate limiting, API key rotation, request logging, anomaly detection, DDoS protection." },
  auth: { title: "Identity & Auth", desc: "SAML/SSO, MFA enforced on all accounts. Role matrix: Physician → Nurse → Front Desk → Billing → Admin. AI gets scoped least-privilege access." },
  waf: { title: "WAF + Firewall", desc: "AWS WAF blocks SQL injection, XSS, bot traffic. All resources deployed inside private VPC subnets — no database ever faces the public internet." },
  audit: { title: "Audit Trail", desc: "CloudTrail logs every API call. Who accessed which PHI, when, from where. Tamper-proof, retained 7 years. Required for HIPAA Technical Safeguards." },
  fastapi: { title: "FastAPI Backend", desc: "Python async API. Handles patient data, clinical workflows, billing logic. Deployed on AWS ECS Fargate. Auto-scales with demand." },
  celery: { title: "Task Queue", desc: "Async jobs: weekly AI reports (Mon 6am), claim status monitoring, lab result notifications, eligibility verification at check-in." },
  fhir: { title: "FHIR R4 Engine", desc: "All data modeled as FHIR resources: Patient, Encounter, Observation, Condition, MedicationRequest, Appointment. Enables interoperability with any FHIR-compliant system." },
  ws: { title: "Real-time Messaging", desc: "FastAPI native WebSockets. End-to-end encrypted messages. HIPAA-compliant alternative to Slack/Teams. TigerConnect or custom build." },
  claude: { title: "Claude API (Anthropic)", desc: "Core AI engine. Clinical documentation drafts, patient triage, billing code suggestions, denial appeal language, weekly executive reports. Every output is a draft until physician-signed." },
  stt: { title: "Speech-to-Text", desc: "AWS Transcribe Medical converts encounter audio to transcript with medical vocabulary. Patient consent captured before recording. Saves physicians 2–3 hrs/day." },
  nlp: { title: "NLP Pipeline", desc: "Extracts ICD-10 diagnosis codes and CPT procedure codes from signed clinical notes. Feeds directly into billing module. Can increase clinic revenue 15–25%." },
  validation: { title: "AI Validator", desc: "Every AI output passes through a validation layer before reaching clinical workflows. Flags hallucinations, missing required fields, unsigned notes blocked from downstream systems." },
  postgres: { title: "PostgreSQL (RDS)", desc: "Primary operational database. AES-256 encryption at rest. Multi-AZ for 99.99% uptime. NEVER hard-delete records — soft deletes with deleted_at timestamps only." },
  replica: { title: "Analytics Replica", desc: "Read-only replica feeds Metabase dashboards. Tracks no-show rates, door-to-provider time, claim denial rates, AI adoption metrics. Zero impact on production performance." },
  s3: { title: "Document Store", desc: "S3 for clinical documents, images, insurance cards, outside records. Versioned, AES-256, lifecycle policies for HIPAA retention. Pre-signed URLs for secure access." },
  kms: { title: "Key Management", desc: "AWS KMS manages all encryption keys. Automatic rotation. Field-level encryption for SSN, DOB, and other high-sensitivity PHI fields in PostgreSQL." },
  lab: { title: "Lab Systems", desc: "Bi-directional HL7 v2 or FHIR integration. Results auto-filed to patient record. AI flags critical values (panic labs) and notifies ordering provider within 60 seconds." },
  pharmacy: { title: "Pharmacy / eRx", desc: "Surescripts integration for e-prescribing. DEA EPCS compliant for controlled substances. Medication history pulled at every encounter." },
  insurance: { title: "Insurance / Payers", desc: "Real-time eligibility verification at check-in via Availity. Copay displayed before patient is seen. Claim submission, status tracking, denial management." },
  comms: { title: "Patient Comms", desc: "Twilio for HIPAA-safe SMS (no PHI in message body — link to secure portal instead). SendGrid for email notifications. Appointment reminders reduce no-shows 30–40%." },
};

export default function ArchDiagram() {
  const [active, setActive] = useState(null);
  const detail = active ? detailMap[active] : null;

  return (
    <div style={{
      background: "#050A14",
      minHeight: "100vh",
      fontFamily: "'Courier New', monospace",
      color: "#E2E8F0",
      padding: "32px 24px",
      position: "relative",
      overflow: "hidden",
    }}>
      {/* Background grid */}
      <div style={{
        position: "fixed", inset: 0, zIndex: 0,
        backgroundImage: "linear-gradient(rgba(14,165,233,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(14,165,233,0.04) 1px, transparent 1px)",
        backgroundSize: "40px 40px",
        pointerEvents: "none",
      }} />

      <div style={{ position: "relative", zIndex: 1, maxWidth: 1100, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: 40 }}>
          <div style={{ fontSize: 11, letterSpacing: 6, color: "#0EA5E9", marginBottom: 8 }}>
            MINDBRIDGE HEALTH AI · SYSTEM ARCHITECTURE
          </div>
          <h1 style={{
            fontSize: 28, fontWeight: 700, margin: 0,
            background: "linear-gradient(90deg, #0EA5E9, #8B5CF6, #10B981)",
            WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
            letterSpacing: 2,
          }}>
            END-TO-END HEALTHCARE INFRASTRUCTURE
          </h1>
          <div style={{ fontSize: 11, color: "#475569", marginTop: 8, letterSpacing: 3 }}>
            HIPAA COMPLIANT · FHIR R4 · AWS · FastAPI · PostgreSQL · Claude API
          </div>
        </div>

        {/* Compliance badges */}
        <div style={{ display: "flex", justifyContent: "center", gap: 12, marginBottom: 36, flexWrap: "wrap" }}>
          {["HIPAA", "FHIR R4", "HL7 v2", "BAA SIGNED", "SOC 2", "AES-256", "MFA ENFORCED"].map(b => (
            <span key={b} style={{
              border: "1px solid rgba(14,165,233,0.3)",
              borderRadius: 3,
              padding: "3px 10px",
              fontSize: 10,
              letterSpacing: 2,
              color: "#0EA5E9",
              background: "rgba(14,165,233,0.06)",
            }}>{b}</span>
          ))}
        </div>

        {/* Layers */}
        {layers.map((layer, li) => (
          <div key={layer.id} style={{ marginBottom: 6 }}>
            {/* Layer label */}
            <div style={{
              fontSize: 10, letterSpacing: 4, color: layer.color,
              marginBottom: 6, paddingLeft: 4,
              borderLeft: `2px solid ${layer.color}`,
              paddingTop: 2, paddingBottom: 2,
            }}>
              {layer.label}
            </div>

            {/* Nodes row */}
            <div style={{
              display: "grid",
              gridTemplateColumns: "repeat(4, 1fr)",
              gap: 8,
              background: `rgba(${layer.color === "#0EA5E9" ? "14,165,233" : layer.color === "#F59E0B" ? "245,158,11" : layer.color === "#8B5CF6" ? "139,92,246" : layer.color === "#10B981" ? "16,185,129" : layer.color === "#EF4444" ? "239,68,68" : "236,72,153"},0.04)`,
              border: `1px solid rgba(${layer.color === "#0EA5E9" ? "14,165,233" : layer.color === "#F59E0B" ? "245,158,11" : layer.color === "#8B5CF6" ? "139,92,246" : layer.color === "#10B981" ? "16,185,129" : layer.color === "#EF4444" ? "239,68,68" : "236,72,153"},0.15)`,
              borderRadius: 6,
              padding: 12,
            }}>
              {layer.nodes.map(node => (
                <button
                  key={node.id}
                  onClick={() => setActive(active === node.id ? null : node.id)}
                  style={{
                    background: active === node.id
                      ? `rgba(${layer.color === "#0EA5E9" ? "14,165,233" : layer.color === "#F59E0B" ? "245,158,11" : layer.color === "#8B5CF6" ? "139,92,246" : layer.color === "#10B981" ? "16,185,129" : layer.color === "#EF4444" ? "239,68,68" : "236,72,153"},0.2)`
                      : "rgba(255,255,255,0.03)",
                    border: `1px solid ${active === node.id ? layer.color : "rgba(255,255,255,0.08)"}`,
                    borderRadius: 6,
                    padding: "12px 10px",
                    cursor: "pointer",
                    textAlign: "left",
                    transition: "all 0.15s ease",
                    boxShadow: active === node.id ? `0 0 16px ${layer.glow}` : "none",
                    color: "#E2E8F0",
                  }}
                  onMouseEnter={e => {
                    if (active !== node.id) {
                      e.currentTarget.style.borderColor = layer.color;
                      e.currentTarget.style.background = `rgba(${layer.color === "#0EA5E9" ? "14,165,233" : layer.color === "#F59E0B" ? "245,158,11" : layer.color === "#8B5CF6" ? "139,92,246" : layer.color === "#10B981" ? "16,185,129" : layer.color === "#EF4444" ? "239,68,68" : "236,72,153"},0.08)`;
                    }
                  }}
                  onMouseLeave={e => {
                    if (active !== node.id) {
                      e.currentTarget.style.borderColor = "rgba(255,255,255,0.08)";
                      e.currentTarget.style.background = "rgba(255,255,255,0.03)";
                    }
                  }}
                >
                  <div style={{ fontSize: 20, marginBottom: 5 }}>{node.icon}</div>
                  <div style={{ fontSize: 11, fontWeight: 700, color: layer.color, letterSpacing: 0.5, marginBottom: 3 }}>
                    {node.label}
                  </div>
                  <div style={{ fontSize: 9.5, color: "#64748B", letterSpacing: 0.3, lineHeight: 1.4 }}>
                    {node.sub}
                  </div>
                </button>
              ))}
            </div>

            {/* Connector arrow */}
            {li < layers.length - 1 && (
              <div style={{ textAlign: "center", padding: "4px 0", color: "#1E3A5F", fontSize: 16 }}>
                ▼
              </div>
            )}
          </div>
        ))}

        {/* Detail panel */}
        {detail && (
          <div style={{
            marginTop: 24,
            background: "rgba(14,165,233,0.06)",
            border: "1px solid rgba(14,165,233,0.3)",
            borderRadius: 8,
            padding: "20px 24px",
            animation: "fadeIn 0.2s ease",
          }}>
            <style>{`@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }`}</style>
            <div style={{ fontSize: 10, letterSpacing: 4, color: "#0EA5E9", marginBottom: 6 }}>COMPONENT DETAIL</div>
            <div style={{ fontSize: 15, fontWeight: 700, color: "#E2E8F0", marginBottom: 8 }}>{detail.title}</div>
            <div style={{ fontSize: 12.5, color: "#94A3B8", lineHeight: 1.7 }}>{detail.desc}</div>
          </div>
        )}

        {/* Data flow legend */}
        <div style={{
          marginTop: 28,
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: 12,
        }}>
          {[
            { icon: "🔒", label: "All PHI encrypted at rest (AES-256) and in transit (TLS 1.3)" },
            { icon: "📝", label: "Every AI output is a DRAFT until physician-signed. Status: draft → reviewed → signed" },
            { icon: "🚫", label: "No hard deletes. All records use soft-delete with deleted_at timestamps" },
          ].map((item, i) => (
            <div key={i} style={{
              background: "rgba(255,255,255,0.02)",
              border: "1px solid rgba(255,255,255,0.06)",
              borderRadius: 6,
              padding: "12px 14px",
              display: "flex",
              gap: 10,
              alignItems: "flex-start",
            }}>
              <span style={{ fontSize: 16, flexShrink: 0 }}>{item.icon}</span>
              <span style={{ fontSize: 10.5, color: "#64748B", lineHeight: 1.5 }}>{item.label}</span>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div style={{ textAlign: "center", marginTop: 28, fontSize: 10, color: "#1E3A5F", letterSpacing: 3 }}>
          MINDBRIDGE HEALTH AI · WEEK 2 · FIDELIS EMMANUEL · HEALTHCARE AI ENGINEER IN TRAINING
        </div>
      </div>
    </div>
  );
}