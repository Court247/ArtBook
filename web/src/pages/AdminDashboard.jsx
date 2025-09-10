import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Trash2, ShieldCheck } from "lucide-react";

const API = import.meta.env.VITE_API_URL;
const AUTH_TOKEN = localStorage.getItem("token");

async function fetchWithAuth(url, method = "GET", body = null) {
  return fetch(`${API}${url}`, {
    method,
    headers: {
      Authorization: `Bearer ${AUTH_TOKEN}`,
      "Content-Type": "application/json",
    },
    ...(body && { body: JSON.stringify(body) }),
  }).then((res) => res.json());
}

export default function AdminDashboard() {
  const [users, setUsers] = useState([]);
  const [posts, setPosts] = useState([]);
  const [flagged, setFlagged] = useState([]);

  useEffect(() => {
    fetchWithAuth("/admin/users").then(setUsers);
    fetchWithAuth("/admin/posts").then(setPosts);
    fetchWithAuth("/admin/flagged-posts").then(setFlagged);
  }, []);

  const deleteUser = async (id) => {
    await fetchWithAuth(`/admin/users/${id}`, "DELETE");
    setUsers(users.filter((u) => u.id !== id));
  };

  const deletePost = async (id) => {
    await fetchWithAuth(`/admin/posts/${id}`, "DELETE");
    setPosts(posts.filter((p) => p.id !== id));
    setFlagged(flagged.filter((p) => p.id !== id));
  };

  const toggleAdmin = async (uid, makeAdmin) => {
    await fetchWithAuth(`/admin/promote-user/${uid}`, "POST", { admin: makeAdmin });
    const refreshed = await fetchWithAuth("/admin/users");
    setUsers(refreshed);
  };

  return (
    <div className="p-4 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-4 flex items-center gap-2">
        <ShieldCheck className="text-green-500" /> Admin Dashboard
      </h1>

      <Tabs defaultValue="users" className="w-full">
        <TabsList>
          <TabsTrigger value="users">Users</TabsTrigger>
          <TabsTrigger value="posts">All Posts</TabsTrigger>
          <TabsTrigger value="flagged">Flagged Posts</TabsTrigger>
        </TabsList>

        {/* USERS TAB */}
        <TabsContent value="users">
          {users.map((user) => (
            <Card key={user.id} className="my-2">
              <CardContent className="flex justify-between items-center p-4">
                <div>
                  <p className="font-semibold">{user.email}</p>
                  <p className="text-sm text-muted">{user.display_name || "Unnamed"}</p>
                  <p className="text-xs">{user.is_admin ? "🛡️ Admin" : "👤 User"}</p>
                </div>
                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    onClick={() => toggleAdmin(user.firebase_uid, !user.is_admin)}
                  >
                    {user.is_admin ? "Demote" : "Promote"}
                  </Button>
                  <Button variant="destructive" onClick={() => deleteUser(user.id)}>
                    <Trash2 className="w-4 h-4 mr-1" /> Delete
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </TabsContent>

        {/* POSTS TAB */}
        <TabsContent value="posts">
          {posts.map((post) => (
            <Card key={post.id} className="my-2">
              <CardContent className="flex justify-between items-center p-4">
                <div>
                  <p className="font-semibold">Post ID: {post.id}</p>
                  <p className="text-sm text-muted">{post.caption}</p>
                </div>
                <Button variant="destructive" onClick={() => deletePost(post.id)}>
                  <Trash2 className="w-4 h-4 mr-1" /> Delete
                </Button>
              </CardContent>
            </Card>
          ))}
        </TabsContent>

        {/* FLAGGED POSTS TAB */}
        <TabsContent value="flagged">
          {flagged.map((post) => (
            <Card key={post.id} className="my-2 border-yellow-500">
              <CardContent className="flex justify-between items-center p-4">
                <div>
                  <p className="font-semibold text-yellow-700">Flagged Post ID: {post.id}</p>
                  <p className="text-sm text-muted">{post.caption}</p>
                </div>
                <Button variant="destructive" onClick={() => deletePost(post.id)}>
                  <Trash2 className="w-4 h-4 mr-1" /> Delete
                </Button>
              </CardContent>
            </Card>
          ))}
        </TabsContent>
      </Tabs>
    </div>
  );
}
