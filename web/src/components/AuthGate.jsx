import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const API = (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(/\/+$/, "");

export default function AuthGate({ children, requireAdmin = false }) {
  const [loading, setLoading] = useState(true);
  const [allowed, setAllowed] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    (async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        navigate("/login");
        return;
      }
      try {
        const res = await fetch(`${API}/users/me`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        if (!res.ok) throw new Error("auth failed");
        const user = await res.json();
        if (requireAdmin && !user.is_admin) {
          navigate("/home");
          return;
        }
        setAllowed(true);
      } catch {
        navigate("/login");
      } finally {
        setLoading(false);
      }
    })();
  }, [requireAdmin, navigate]);

  if (loading) return <div style={{ padding: 20 }}>Checking access...</div>;
  if (!allowed) return null;
  return children;
}
