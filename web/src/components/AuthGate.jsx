import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Spinner from "./Spinner";

export default function AuthGate({ children, requireAdmin = false }) {
  const [loading, setLoading] = useState(true);
  const [allow, setAllow] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return navigate("/");

    fetch(`${import.meta.env.VITE_API_URL}/users/me`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((user) => {
        if (requireAdmin && !user.is_admin) {
          navigate("/home");
        } else {
          setAllow(true);
        }
      })
      .catch(() => navigate("/"))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Spinner />;
  return allow ? children : null;
}
