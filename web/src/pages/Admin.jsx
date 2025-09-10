import AdminDashboard from "./AdminDashboard";
import AuthGate from "../components/AuthGate";

export default function AdminPage() {
  return (
    <AuthGate requireAdmin={true}>
      <AdminDashboard />
    </AuthGate>
  );
}
