// src/pages/LoginPage.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "../firebase";

export default function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");

  const handleLogin = async () => {
    setErr("");
    try {
      const cred = await signInWithEmailAndPassword(auth, email, password);
      const token = await cred.user.getIdToken();
      localStorage.setItem("token", token);
      navigate("/home");
    } catch (e) {
      setErr(e.message);
    }
  };

  return (
    <div className="login-page">
      <h2>Login</h2>
      {err && <div className="error">{err}</div>}
      <input
        className="input email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        className="input password"
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button className="btn login" onClick={handleLogin}>
        Sign In
      </button>
      <button
        className="btn register"
        onClick={() => navigate("/register")}
      >
        Create Account
      </button>
    </div>
  );
}
