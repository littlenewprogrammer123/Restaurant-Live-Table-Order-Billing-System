import { useState } from "react";
import api from "../api";

export default function Register({ onBack }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("Waiter");
  const [error, setError] = useState("");

  const handleRegister = async () => {
  try {
    await api.post("auth/register/", {
      username,
      password,
      role,
    });

    alert("Registration successful. Please login.");
    onBack(); // go back to Login page
  } catch (err) {
    if (err.response) {
      setError(err.response.data.error || "Registration failed");
    } else {
      setError("Server error");
    }
  }
};

const res = await api.post("auth/register/", {
  username,
  password,
  role,
});
onLogin(res.data.role);


  return (
    <div className="card">
      <h2>Register</h2>

      {error && <p className="error">{error}</p>}

      <input
        placeholder="Username"
        onChange={(e) => setUsername(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />

      <select onChange={(e) => setRole(e.target.value)}>
        <option value="Waiter">Waiter</option>
        <option value="Cashier">Cashier</option>
        <option value="Manager">Manager</option>
      </select>

      <button onClick={handleRegister}>Register</button>
      <button className="secondary" onClick={onBack}>Back to Login</button>
    </div>
  );
}
