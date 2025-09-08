import React, { useEffect, useMemo, useState } from "react";
import "./recommend.css";

const API_BASE =
  process.env.REACT_APP_API_URL?.replace(/\/$/, "") || "http://127.0.0.1:8000";

const emptyResume = {
  summary: "",
  skills: "",
  education: "",
  projects: "",
  experience: "",
  certifications: "",
};

function Field({ label, name, value, onChange, placeholder, rows = 4 }) {
  return (
    <div className="field">
      <label htmlFor={name} className="label">
        {label}
      </label>
      <textarea
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        rows={rows}
        className="textarea"
      />
    </div>
  );
}

function RecommendationItem({ item, onClick }) {
  return (
    <button
      className="rec-item"
      onClick={onClick}
      aria-label={`Open ${item.title}`}
    >
      <div className="rec-item-main">
        <div className="rec-title">{item.title || "Untitled Role"}</div>
        <div className="rec-meta">
          <span className="pill neutral">{item.company || "Unknown Org"}</span>
          <span className="dot" />
          <span className="subtle">{item.location || "Remote/Unknown"}</span>
        </div>
      </div>
      <svg
        className="chev"
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden="true"
      >
        <path d="M9 18l6-6-6-6" />
      </svg>
    </button>
  );
}

function RecommendationSkeleton() {
  return (
    <div className="rec-item skeleton">
      <div className="skeleton-line w-60" />
      <div className="rec-meta">
        <span className="skeleton-pill" />
        <span className="dot" />
        <span className="skeleton-line w-30" />
      </div>
    </div>
  );
}

export default function RecommendPage() {
  const [resume, setResume] = useState(emptyResume);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [selected, setSelected] = useState(null);

  // Load from localStorage if available
  useEffect(() => {
    try {
      const saved = localStorage.getItem("resumeDraft");
      if (saved) {
        setResume(JSON.parse(saved));
      }
    } catch (e) {
      // ignore parse errors
    }
  }, []);

  // Persist draft
  useEffect(() => {
    try {
      localStorage.setItem("resumeDraft", JSON.stringify(resume));
    } catch (e) {
      // ignore quota errors
    }
  }, [resume]);

  const formValid = useMemo(() => {
    // at least one field must be filled to call API meaningfully
    return Object.values(resume).some((v) => (v || "").trim().length > 0);
  }, [resume]);

  function onChange(e) {
    const { name, value } = e.target;
    setResume((r) => ({ ...r, [name]: value }));
  }

  async function handleRecommend(e) {
    e?.preventDefault?.();
    setErr("");
    setLoading(true);
    setRecommendations([]);
    setSelected(null);
    setDrawerOpen(false);

    try {
      const res = await fetch(`${API_BASE}/recommend/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(resume),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || `Request failed with ${res.status}`);
      }

      const data = await res.json();
      setRecommendations(Array.isArray(data) ? data : []);
    } catch (error) {
      setErr(
        error?.message ||
          "Something went wrong while fetching recommendations.",
      );
    } finally {
      setLoading(false);
    }
  }

  function openDrawer(item) {
    setSelected(item);
    setDrawerOpen(true);
  }

  function closeDrawer() {
    setDrawerOpen(false);
    // delay clearing selection so exit animation can finish
    setTimeout(() => setSelected(null), 220);
  }

  function fillSample() {
    setResume({
      summary:
        "CS student passionate about NLP and computer vision. Seeking impactful internships where I can ship features fast.",
      skills:
        "Python, JavaScript, React, FastAPI, SQL, PyTorch, TensorFlow, Docker, Git, Linux",
      education:
        "B.S. in Computer Science, State University (2022–2026), GPA: 3.8/4.0",
      projects:
        "Built semantic search with SentenceTransformers; Deployed a React + FastAPI app on Docker; Implemented a vision classifier with transfer learning.",
      experience:
        "Teaching Assistant for Data Structures; Software Intern at StartupX (React + FastAPI); Research assistant for NLP lab.",
      certifications:
        "AWS Cloud Practitioner; TensorFlow Developer Certificate",
    });
  }

  function clearAll() {
    setResume(emptyResume);
    setRecommendations([]);
    setSelected(null);
    setDrawerOpen(false);
    setErr("");
  }

  // Close drawer on Escape
  useEffect(() => {
    function onKey(e) {
      if (e.key === "Escape" && drawerOpen) closeDrawer();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [drawerOpen]);

  return (
    <div className="recommend-page">
      {/* Left: Resume */}
      <section className="pane resume-pane">
        <header className="pane-header">
          <div className="title-wrap">
            <div className="dot-accent" />
            <h1 className="title">Resume</h1>
          </div>
          <div className="header-actions">
            <button className="btn ghost" onClick={fillSample}>
              Prefill sample
            </button>
            <button className="btn ghost" onClick={clearAll}>
              Clear
            </button>
          </div>
        </header>

        <form className="resume-form" onSubmit={handleRecommend}>
          <Field
            label="Summary"
            name="summary"
            value={resume.summary}
            onChange={onChange}
            placeholder="A brief professional summary..."
            rows={3}
          />
          <Field
            label="Skills"
            name="skills"
            value={resume.skills}
            onChange={onChange}
            placeholder="List your skills (comma-separated)…"
            rows={2}
          />
          <Field
            label="Education"
            name="education"
            value={resume.education}
            onChange={onChange}
            placeholder="Degree, institution, graduation year…"
          />
          <Field
            label="Projects"
            name="projects"
            value={resume.projects}
            onChange={onChange}
            placeholder="Highlight a few projects, tech stack, outcomes…"
          />
          <Field
            label="Experience"
            name="experience"
            value={resume.experience}
            onChange={onChange}
            placeholder="Roles, responsibilities, achievements…"
          />
          <Field
            label="Certifications"
            name="certifications"
            value={resume.certifications}
            onChange={onChange}
            placeholder="Relevant certifications…"
            rows={2}
          />

          <div className="form-actions">
            <button
              className="btn primary"
              type="submit"
              disabled={!formValid || loading}
            >
              {loading ? (
                <>
                  <span className="spinner" /> Generating…
                </>
              ) : (
                "Get Recommendations"
              )}
            </button>
            {!formValid && (
              <div className="hint">Add at least one field to enable.</div>
            )}
          </div>
        </form>
      </section>

      {/* Right: Recommendations */}
      <section className="pane results-pane">
        <header className="pane-header">
          <div className="title-wrap">
            <div className="dot-accent" />
            <h2 className="title">Recommendations</h2>
          </div>
          <div className="count-badge">
            {loading ? "…" : recommendations.length}
          </div>
        </header>

        <div className="results-body">
          {err && <div className="error">{err}</div>}

          {!loading && recommendations.length === 0 && !err && (
            <div className="empty">
              <div className="empty-emoji">🔍</div>
              <div className="empty-title">No recommendations yet</div>
              <div className="empty-sub">
                Fill in your resume on the left and click “Get Recommendations.”
              </div>
            </div>
          )}

          {loading && (
            <div className="list">
              {Array.from({ length: 5 }, (_, i) => (
                <RecommendationSkeleton key={i} />
              ))}
            </div>
          )}

          {!loading && recommendations.length > 0 && (
            <div className="list">
              {recommendations.map((item, idx) => (
                <RecommendationItem
                  key={`${item.title}-${item.company}-${idx}`}
                  item={item}
                  onClick={() => openDrawer(item)}
                />
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Drawer for full details */}
      <div
        className={`drawer ${drawerOpen ? "open" : ""}`}
        aria-hidden={!drawerOpen}
      >
        <div className="drawer-header">
          <div className="drawer-titles">
            <div className="drawer-title">{selected?.title}</div>
            <div className="drawer-sub">
              <span className="pill neutral">{selected?.company}</span>
              <span className="dot" />
              <span className="subtle">{selected?.location}</span>
            </div>
          </div>
          <button className="icon-btn" onClick={closeDrawer} aria-label="Close">
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M18 6L6 18" />
              <path d="M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="drawer-content">
          <div className="drawer-section">
            <div className="section-title">Description</div>
            <p className="section-body">
              {selected?.description || "No description provided."}
            </p>
          </div>

          <div className="drawer-section">
            <div className="section-title">Requirements</div>
            <p className="section-body">
              {selected?.requirements || "No requirements provided."}
            </p>
          </div>
        </div>
      </div>

      {/* Backdrop */}
      {drawerOpen && <div className="backdrop" onClick={closeDrawer} />}
    </div>
  );
}
