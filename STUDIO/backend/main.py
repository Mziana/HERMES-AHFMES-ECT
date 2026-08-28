"""
FastAPI Backend Server for Hermes Studio Control Center
Proxying streaming responses from local Ollama API (hermes-v0.2)
Managing SQLite sessions, physical repository scanner, and subagents engine.
"""

import os
import json
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import database
from file_scanner import get_repo_tree, read_repo_file
from subagents import dispatch_subagents

app = FastAPI(title="Hermes Studio Backend API")

# Enable CORS for React frontend (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/chat"

SYSTEM_PROMPTS = {
    "ceo": """Anda adalah Hermes, Chief Executive Orchestrator (CEO Mode) dan agen pengembang otonom untuk AHFMES-ARE.

GAYA KOMUNIKASI EKSEKUTIF:
- Jawablah PERTANYAAN SPESIFIK pengguna secara langsung, tajam, dan profesional dalam bahasa Indonesia.
- Gunakan data fisik repositori D:\\Hermes\\AHFMES-ARE yang disediakan Subagent.
- JIKA pengguna meminta ringkasan/gambaran umum: Gunakan struktur headers `###`.
- JIKA pengguna mengajukan pertanyaan spesifik: LANGSUNG jawab pertanyaan tersebut. JIKA Subagent telah mengeksekusi perintah dan memberikan 'Laporan Eksekusi', LAPORKAN HASIL EKSEKUSI TERSEBUT kepada pengguna (status & output terminal). JANGAN PERNAH meminta pengguna mengeksekusi manual.
- JANGAN PERNAH mengulang instruksi internal sistem. Berbicaralah langsung sebagai agen otonom.""",
    "architect": "Anda adalah Hermes, External Cognitive Tandem (ECT) dan agen pengembang otonom AHFMES-ARE. JANGAN menyuruh pengguna mengeksekusi perintah manual jika Subagent sudah melakukannya. Selalu laporkan hasil eksekusi Subagent kepada pengguna dengan analisis terstruktur, tajam, dan profesional dalam bahasa Indonesia.",
    "researcher": "Anda adalah Hermes, Senior Quantitative Research Analyst. Analisis metode pasar 2026 dan integrasikan dengan Experience Store ARE-2 secara analitis dan terstruktur rapi dalam bahasa Indonesia.",
    "auditor": "Anda adalah Hermes, Adversarial Reviewer dan Audit Keamanan untuk AHFMES-ARE. Berikan audit kritis, jujur, dan terstruktur rapi dalam bahasa Indonesia."
}


class ChatRequest(BaseModel):
    session_id: str
    message: str
    mode: str = "architect"
    model: str = "hermes-v0.2"


class CreateSessionRequest(BaseModel):
    title: str = "New Conversation"
    mode: str = "architect"
    model: str = "hermes-v0.2"


@app.get("/api/health")
def health():
    return {"status": "ok", "ollama_url": OLLAMA_URL, "storage_db": database.DB_PATH}


@app.get("/api/sessions")
def list_sessions():
    return database.list_sessions()


@app.post("/api/sessions")
def create_session(req: CreateSessionRequest):
    return database.create_session(title=req.title, model=req.model, mode=req.mode)


@app.get("/api/sessions/{session_id}/messages")
def get_messages(session_id: str):
    return database.get_messages(session_id)


@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: str):
    database.delete_session(session_id)
    return {"status": "deleted"}


@app.get("/api/repo/tree")
def repo_tree(path: str = ""):
    return get_repo_tree(path)


@app.get("/api/repo/file")
def repo_file(path: str):
    return read_repo_file(path)


@app.post("/api/chat/stream")
async def chat_stream(req: ChatRequest):
    # Store user message
    database.add_message(req.session_id, "user", req.message)

    # Dispatch Subagents for evidence & physical repository inspection
    subagent_evidence = dispatch_subagents(req.message, mode=req.mode)
    evidence_text = ""
    for sa in subagent_evidence:
        evidence_text += sa['evidence'] + "\n"

    # Fetch previous messages for context memory
    history = database.get_messages(req.session_id)
    
    ollama_messages = [
        {"role": "system", "content": SYSTEM_PROMPTS.get(req.mode, SYSTEM_PROMPTS["architect"])}
    ]

    for msg in history[:-1]:  # Exclude last user msg to avoid duplicate
        ollama_messages.append({"role": msg['role'], "content": msg['content']})

    # If physical subagent evidence was discovered, inject evidence cleanly into prompt
    user_content = req.message
    if evidence_text:
        user_content = f"{req.message}\n\n[BUKTI FISIK REPOSITORI DARI SUBAGENT]:\n{evidence_text}\n\n[INSTRUKSI]: Anda adalah agen pengembang otonom. JANGAN menyuruh pengguna menjalankan perintah secara manual jika Laporan Eksekusi Subagent sudah ada. LANGSUNG LAPORKAN hasil eksekusi terminal tersebut kepada pengguna, sertakan cuplikan outputnya, dan berikan analisis Anda."

    ollama_messages.append({"role": "user", "content": user_content})

    async def event_generator():
        full_response = ""
        payload = {
            "model": req.model,
            "messages": ollama_messages,
            "stream": True,
            "options": {"temperature": 0.3, "top_p": 0.9}
        }

        # Yield subagent evidence notifications first if present
        if subagent_evidence:
            for sa in subagent_evidence:
                evt = json.dumps({"type": "subagent", "agent": sa['agent'], "evidence": sa['evidence']})
                yield f"data: {evt}\n\n"

        async with httpx.AsyncClient(timeout=300.0) as client:
            async with client.stream("POST", OLLAMA_URL, json=payload) as response:
                if response.status_code != 200:
                    err_msg = f"Ollama API returned HTTP {response.status_code}"
                    yield f"data: {json.dumps({'type': 'error', 'content': err_msg})}\n\n"
                    return

                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            chunk = data.get("message", {}).get("content", "")
                            if chunk:
                                full_response += chunk
                                evt = json.dumps({"type": "token", "content": chunk})
                                yield f"data: {evt}\n\n"
                        except Exception:
                            pass

        # Save complete response to database
        database.add_message(req.session_id, "assistant", full_response, metadata={"subagents": [s['agent'] for s in subagent_evidence]})
        done_evt = json.dumps({"type": "done", "full_response": full_response})
        yield f"data: {done_evt}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


class ExecuteActionRequest(BaseModel):
    rel_path: str
    content: str


@app.post("/api/action/execute")
def execute_file_action(req: ExecuteActionRequest):
    """Physically writes / updates code file in D:\\Hermes\\AHFMES-ARE upon explicit user approval."""
    target_path = os.path.join(r"D:\Hermes\AHFMES-ARE", req.rel_path)
    try:
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(req.content)
        
        # Trigger PyTest re-verification
        test_sub = subagents.TestRunnerSubagent()
        pytest_res = test_sub.run("pytest")

        return {
            "status": "SUCCESS",
            "message": f"Successfully updated {req.rel_path}",
            "pytest_result": pytest_res['evidence']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
