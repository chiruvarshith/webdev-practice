import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; 
import rightImg from '../assets/icons/right_img.png';
import leftImg from '../assets/icons/left_img.png';

function Admin() {
    const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const [error, setError] = useState(""); // Add state for error message

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Check if the username and password match the required values
    if (formData.username === "sample" && formData.password === "123456789") {
      // Navigate to /home if the credentials are correct
      navigate("/form")
    } else {
      // Display an error message if the credentials are incorrect
      setError("Invalid username or password");
    }
  };

  return (
    <div>
      <div className="bg-green-800 text-black h-20 p-2 flex items-center justify-between" style={{ background: "greenyellow", justifyContent: "center", alignItems: "center" }}>
        <div className="flex items-center" style={{ display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center" }}>
          <h2 className="text-xl font-bold">
            ADVANCED INSTITUTE FOR WILDLIFE CONSERVATION
          </h2>

          <p>
            A Government of Tamil Nadu Institute
          </p>
        </div>
      </div>
      <form onSubmit={handleSubmit} style={{ color: "black", display: "flex", flexDirection: "column", alignItems: "center" }}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleInputChange}
          style={{ margin: "10px", padding: "5px" }}
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleInputChange}
          style={{ margin: "10px", padding: "5px" }}
        />
        <button type="submit" style={{ color: "black", margin: "10px", padding: "5px" }}>Submit</button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default Admin;