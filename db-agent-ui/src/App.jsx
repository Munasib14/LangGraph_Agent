import React, { useState, useEffect } from "react";
import "./App.css";
import AgentSelector from "./components/AgentSelector";
import PromptDropdown from "./components/PromptDropdown";
import SqlEditor from "./components/SqlEditor";
import FileUploader from "./components/FileUploader";
import axios from "axios";

const promptMap = {
  "DB Agent": [
    "transform_identity.j2",
    "optimize_performance.j2",
    "migrate_legacy_azure.j2",
    "refactor_procedure.j2",
    "best_practices.j2",
    "add_try_catch.j2",
    "analyze_security_risks.j2",
  ],
  "Web Agent": ["optimize_css.j2", "convert_html_to_jsx.j2"],
  "DevOps Agent": ["dockerize_app.j2", "ci_cd_pipeline.j2"],
  "Test Agent": ["generate_unit_tests.j2"],
  "Batch Jobs Agent": ["schedule_batch_cron.j2"],
};

function App() {
  const [selectedAgent, setSelectedAgent] = useState("DB Agent");
  const [promptList, setPromptList] = useState(promptMap["DB Agent"]);
  const [selectedPrompt, setSelectedPrompt] = useState("");
  const [editablePrompt, setEditablePrompt] = useState("");
  const [sqlCode, setSqlCode] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  useEffect(() => {
    setPromptList(promptMap[selectedAgent] || []);
    setSelectedPrompt("");
    setEditablePrompt("");
    setSqlCode("");
    setChatHistory([]);
  }, [selectedAgent]);

  useEffect(() => {
    const fetchPrompt = async () => {
      if (!selectedPrompt) return;
      try {
        const res = await axios.get(`http://127.0.0.1:8000/get-prompt/${selectedPrompt}`);
        const content = res?.data?.prompt_content || "";
        setEditablePrompt(content);
        setSqlCode(content);
      } catch {
        const fallback = "-- ⚠️ Unable to fetch prompt.";
        setEditablePrompt(fallback);
        setSqlCode(fallback);
      }
    };
    fetchPrompt();
  }, [selectedPrompt]);

  const handleRun = async () => {
    if (!sqlCode.trim()) {
      alert("⚠️ Please enter SQL code.");
      return;
    }

    try {
      const res = await axios.post("http://127.0.0.1:8000/run-db-agent/", {
        sql_code: sqlCode,
        prompt_name: selectedPrompt || "transform_identity.j2",
      });
      const agentResponse = res?.data?.result?.output || "⚠️ No output returned.";
      setChatHistory((prev) => [...prev, { user: sqlCode, agent: agentResponse }]);
      setSqlCode("");
    } catch (err) {
      const errorMsg = "❌ Error: " + (err?.response?.data?.detail || err.message);
      setChatHistory((prev) => [...prev, { user: sqlCode, agent: errorMsg }]);
    }
  };

  return (
    <>
      <div className="header">
        <div className="title">GENAI COE-CHATBOT</div>
        <div className="username">Arjun Swarna</div>
      </div>

      <div className="container">
        <div className="left-panel">
          <div className="chat-wrapper">
            {[...chatHistory].reverse().map((item, idx) => (
              <div key={idx} className="chat-block">
                <div className="user-msg"><strong>User:</strong> <pre>{item.user}</pre></div>
                <div className="agent-msg"><strong>Agent:</strong> <pre>{item.agent}</pre></div>
              </div>
            ))}
          </div>

          <h4>Agent Input :</h4>
          <SqlEditor
            value={sqlCode}
            onChange={setSqlCode}
            placeholder="Paste or write SQL/Code to be analyzed, transformed, or optimized..."
          />
          <button className="run-btn" onClick={handleRun}>ENTER</button>
        </div>

        <div className="right-panel">
          <AgentSelector selected={selectedAgent} onChange={setSelectedAgent} />
          <PromptDropdown
            prompts={promptList}
            selectedPrompt={selectedPrompt}
            editablePrompt={editablePrompt}
            onSelect={setSelectedPrompt}
            onEdit={setEditablePrompt}
            onUpdate={(updated) => {
              setPromptList((prev) =>
                prev.map((p) => (p === selectedPrompt ? updated : p))
              );
              setSelectedPrompt(updated);
              setEditablePrompt("");
              setSqlCode(updated);
            }}
            onDelete={() => {
              setPromptList((prev) => prev.filter((p) => p !== selectedPrompt));
              setSelectedPrompt("");
              setEditablePrompt("");
              setSqlCode("");
            }}
          />
          <FileUploader />
        </div>
      </div>
    </>
  );
}

export default App;