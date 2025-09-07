// src/pages/recommend/recommend.js

import React, { useState } from "react";
import axios from "axios"; // We'll use axios to make the API request
import "./recommend.css"; // Import our stylesheet

const RecommendPage = () => {
  // 1. STATE MANAGEMENT
  // We use 'useState' to store data that can change over time.

  // Store the form data from the user's input
  const [resumeData, setResumeData] = useState({
    summary:
      "Experienced software developer with a background in machine learning and cloud computing.",
    skills: "Python, JavaScript, React, FastAPI, Docker, AWS",
    education: "B.S. in Computer Science",
    projects: "Developed a real-time recommendation engine for e-commerce.",
    experience: "Software Engineer at Tech Corp, focused on backend services.",
    certifications: "AWS Certified Developer",
  });

  // Store the list of recommended internships from the API
  const [recommendations, setRecommendations] = useState([]);

  // Store the loading state (to show a spinner or message)
  const [isLoading, setIsLoading] = useState(false);

  // Store any potential errors from the API call
  const [error, setError] = useState(null);

  // 2. EVENT HANDLERS
  // These functions handle user interactions.

  // This function updates the 'resumeData' state whenever a user types in a form field.
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setResumeData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  // This function is called when the form is submitted.
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevents the default browser action of refreshing the page on form submit.

    setIsLoading(true); // Set loading to true to show a loading message
    setError(null); // Clear any previous errors
    setRecommendations([]); // Clear previous recommendations

    try {
      // THE API CALL!
      // We use axios.post to send a POST request.
      // The first argument is the API endpoint URL.
      // The second argument is the data we want to send in the request body (our resume data).
      const response = await axios.post(
        "http://127.0.0.1:8000/recommend/",
        resumeData,
      );

      // If the call is successful, we update our state with the data from the API.
      setRecommendations(response.data);
    } catch (err) {
      // If there's an error...
      console.error("API Error:", err);
      setError(
        "Failed to fetch recommendations. Please make sure the API server is running and reachable.",
      );
    } finally {
      // This runs whether the request was successful or not.
      setIsLoading(false); // Set loading to false to hide the loading message
    }
  };

  // 3. JSX (The UI)
  // This is what gets rendered to the screen.
  return (
    <div className="recommend-container">
      <h1>Internship Recommender</h1>
      <div className="main-content">
        {/* Left Side: The Form */}
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

        {/* Right Side: The Results */}
        <div className="results-section">
          <h2>Recommended Internships</h2>
          {isLoading && (
            <div className="loading-message">
              Finding the best matches for you...
            </div>
          )}
          {error && <div className="error-message">{error}</div>}

          {/* We only show recommendations if loading is false and there are recommendations to show */}
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
          {/* Show a placeholder if there are no results yet */}
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
