// src/components/AdminDashboard.jsx
import { useEffect, useState } from "react";
import { auth } from "../firebase";

export default function AdminDashboard() {
  const [users, setUsers] = useState([]);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  const API = import.meta.env.VITE_API_URL;

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = await auth.currentUser.getIdToken();

        const [usersRes, postsRes] = await Promise.all([
          fetch(`${API}/admin/users`, {
            headers: { Authorization: `Bearer ${token}` },
          }),
          fetch(`${API}/admin/posts`, {
            headers: { Authorization: `Bearer ${token}` },
          }),
        ]);

        if (usersRes.ok) setUsers(await usersRes.json());
        if (postsRes.ok) setPosts(await postsRes.json());
      } catch (err) {
        console.error("Error loading admin data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [API]);

  if (loading) return <p>Loading admin data...</p>;

  return (
    <div style={{ padding: "1rem" }}>
      <h3>Admin Dashboard</h3>

      <section>
        <h4>Users</h4>
        {users.length === 0 ? (
          <p>No users found.</p>
        ) : (
          <ul>
            {users.map((u) => (
              <li key={u.id}>
                {u.email} {u.is_admin && "(Admin)"}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section style={{ marginTop: "1rem" }}>
        <h4>Posts</h4>
        {posts.length === 0 ? (
          <p>No posts found.</p>
        ) : (
          <ul>
            {posts.map((p) => (
              <li key={p.id}>
                {p.caption} (by user {p.user_id})
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
