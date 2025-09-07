import React, { useState } from "react";
import axios from "axios";
import "./recommend.css";

const RecommendPage = () => {
  const [resumeData, setResumeData] = useState({
    summary:
      "Experienced software developer with a background in machine learning and cloud computing.",
    skills: "Python, JavaScript, React, FastAPI, Docker, AWS",
    education: "B.S. in Computer Science",
    projects: "Developed a real-time recommendation engine for e-commerce.",
    experience: "Software Engineer at Tech Corp, focused on backend services.",
    certifications: "AWS Certified Developer",
  });

  const [recommendations, setRecommendations] = useState([]);

  const [isLoading, setIsLoading] = useState(false);

  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setResumeData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setIsLoading(true);
    setError(null);
    setRecommendations([]);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/recommend/",
        resumeData,
      );

      setRecommendations(response.data);
    } catch (err) {
      console.error("API Error:", err);
      setError(
        "Failed to fetch recommendations. Please make sure the API server is running and reachable.",
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="recommend-container">
      <h1>Internship Recommender</h1>
      <div className="main-content">
        <form onSubmit={handleSubmit} className="resume-form">
          <h2>Enter Your Resume Details</h2>

          <div className="form-group">
            <label>Summary</label>
            <textarea
              name="summary"
              value={resumeData.summary}
              onChange={handleInputChange}
            />
          </div>

          <div className="form-group">
            <label>Skills</label>
            <input
              type="text"
              name="skills"
              value={resumeData.skills}
              onChange={handleInputChange}
            />
          </div>

          <div className="form-group">
            <label>Education</label>
            <input
              type="text"
              name="education"
              value={resumeData.education}
              onChange={handleInputChange}
            />
          </div>

          <div className="form-group">
            <label>Projects</label>
            <textarea
              name="projects"
              value={resumeData.projects}
              onChange={handleInputChange}
            />
          </div>

          <div className="form-group">
            <label>Experience</label>
            <textarea
              name="experience"
              value={resumeData.experience}
              onChange={handleInputChange}
            />
          </div>

          <div className="form-group">
            <label>Certifications</label>
            <input
              type="text"
              name="certifications"
              value={resumeData.certifications}
              onChange={handleInputChange}
            />
          </div>

          <button type="submit" className="submit-btn" disabled={isLoading}>
            {isLoading ? "Analyzing..." : "Get Recommendations"}
          </button>
        </form>

        <div className="results-section">
          <h2>Recommended Internships</h2>
          {isLoading && (
            <div className="loading-message">
              Finding the best matches for you...
            </div>
          )}
          {error && <div className="error-message">{error}</div>}

          {!isLoading &&
            recommendations.length > 0 &&
            recommendations.map((internship, index) => (
              <div key={index} className="internship-card">
                <h3>{internship.title}</h3>
                <div className="company-location">
                  {internship.company} - {internship.location}
                </div>
                <h4>Description</h4>
                <p>{internship.description}</p>
                <h4>Requirements</h4>
                <p>{internship.requirements}</p>
              </div>
            ))}
          {!isLoading && !error && recommendations.length === 0 && (
            <div className="loading-message">
              Your recommendations will appear here.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default RecommendPage;
