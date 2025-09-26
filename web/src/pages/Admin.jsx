// src/pages/Admin.jsx
import AdminDashboard from "../components/AdminDashboard";
import AuthGate from "../components/AuthGate";

export default function Admin() {
  return (
    <AuthGate requireAdmin>
      <AdminDashboard />
    </AuthGate>
  );
}
