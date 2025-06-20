// src/pages/HomePage.jsx
import { useNavigate } from "react-router-dom";
import { auth } from "../firebase";

export default function HomePage() {
  const navigate = useNavigate();

  const logout = async () => {
    await auth.signOut();
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl mb-4">Welcome Home!</h1>
      <button onClick={logout} className="bg-red-500 px-4 py-2 rounded text-white">
        Log out
      </button>
    </div>
  );
}
