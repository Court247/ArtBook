// src/pages/HomePage.jsx
import { signOut } from "firebase/auth";
import { auth } from "../firebase";
import { useNavigate } from "react-router-dom";

export default function HomePage() {
  const navigate = useNavigate();

  const handleLogout = async () => {
    await signOut(auth);
    navigate("/login");
  };

  return (
    <>
      <h2>Welcome to ArtBook!</h2>
      <button onClick={handleLogout}>Logout</button>
    </>
  );
}
