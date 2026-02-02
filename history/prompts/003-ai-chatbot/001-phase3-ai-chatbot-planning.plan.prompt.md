---
id: 001
title: Phase 3 AI Chatbot Planning
stage: plan
date: 2026-02-02
surface: agent
model: claude-opus-4-5-20251101
feature: 003-ai-chatbot
branch: 003-ai-chatbot
user: developer
command: /sp.plan
labels: ["planning", "ai-chatbot", "phase-3", "openai", "tools"]
links:
  spec: specs/003-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-ai-chatbot/plan.md
  - specs/003-ai-chatbot/research.md
  - specs/003-ai-chatbot/data-model.md
  - specs/003-ai-chatbot/quickstart.md
  - specs/003-ai-chatbot/contracts/chat-api.yaml
  - specs/003-ai-chatbot/contracts/tools.md
tests:
  - N/A (planning phase)
---

## Prompt

User invoked /sp.plan command to execute the implementation planning workflow for the AI-Powered Todo Chatbot (Phase 3) feature. The spec was previously approved with status "Approved".

## Response snapshot

Completed Phase 0 (Research) and Phase 1 (Design & Contracts) for Phase 3 AI Chatbot:

**Research Phase (research.md)**:
- Decided on OpenAI SDK with gpt-4o-mini model
- Chose direct Python tool functions over MCP server
- PostgreSQL for conversation storage
- 50 message context limit
- Request-response pattern (no WebSocket)
- Security: system prompt hardening + user isolation

**Design Phase**:
- Created data-model.md with Conversation and Message entities
- Created OpenAPI spec (chat-api.yaml) for POST /api/chat
- Created tool contracts (tools.md) for 5 tools
- Created quickstart.md for setup guide

**Implementation Plan**:
- 5 phases: Backend Foundation → AI Agent & Tools → Chat API → Frontend Chat UI → Integration & Polish
- New dependencies: openai>=1.0.0
- New env vars: OPENAI_API_KEY, OPENAI_MODEL, MAX_CONVERSATION_MESSAGES

## Outcome

- ✅ Impact: Complete planning artifacts ready for task generation
- 🧪 Tests: N/A (planning phase)
- 📁 Files: 6 artifacts created (plan.md, research.md, data-model.md, quickstart.md, chat-api.yaml, tools.md)
- 🔁 Next prompts: Run /sp.tasks to generate implementation tasks
- 🧠 Reflection: Architecture decisions favor simplicity - direct tool functions over MCP, HTTP over WebSocket

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
