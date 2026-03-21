import { useState } from "react";
import { useNavigate } from "react-router";
import { Activity, Shield } from "lucide-react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";

export function Login() {
  const navigate      = useNavigate();
  const [username,  setUsername]  = useState("");
  const [password,  setPassword]  = useState("");
  const [error,     setError]     = useState("");
  const [loading,   setLoading]   = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res  = await fetch("http://localhost:8000/api/login", {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify({ username, password }),
      });
      const data = await res.json();
      if (data.success) {
        localStorage.setItem("role",     data.role);
        localStorage.setItem("username", data.username);
        navigate("/dashboard");
      } else {
        setError("Invalid username or password");
      }
    } catch {
      setError("Cannot connect to server. Make sure API is running on port 8000.");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#F8FAFC] via-[#EFF6FF] to-[#F8FAFC] flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="bg-[#2563EB] p-4 rounded-2xl shadow-lg">
              <Activity className="w-12 h-12 text-white" />
            </div>
          </div>
          <h1 className="text-3xl font-bold text-[#1E293B] mb-2">NurseGuard</h1>
          <p className="text-[#64748B]">AI-powered Nurse Fatigue Management</p>
        </div>
        <div className="bg-white rounded-xl shadow-lg p-8 border border-[#E2E8F0]">
          <form onSubmit={handleLogin} className="space-y-6">
            <div>
              <Label htmlFor="username" className="text-[#1E293B]">Username</Label>
              <Input id="username" type="text" placeholder="Enter your username"
                value={username} onChange={(e) => setUsername(e.target.value)}
                className="mt-2 bg-[#F8FAFC] border-[#E2E8F0]" required />
            </div>
            <div>
              <Label htmlFor="password" className="text-[#1E293B]">Password</Label>
              <Input id="password" type="password" placeholder="Enter your password"
                value={password} onChange={(e) => setPassword(e.target.value)}
                className="mt-2 bg-[#F8FAFC] border-[#E2E8F0]" required />
            </div>
            {error && <p className="text-red-500 text-sm">{error}</p>}
            <Button type="submit" disabled={loading}
              className="w-full bg-[#2563EB] hover:bg-[#1D4ED8] text-white py-6">
              {loading ? "Logging in..." : "Login"}
            </Button>
          </form>
          <div className="mt-4 text-center">
            <p className="text-xs text-[#64748B]">admin/admin123 · nurse1/nurse123 · manager/manager123</p>
          </div>
        </div>
        <div className="mt-6 flex items-center justify-center gap-2 text-sm text-[#64748B]">
          <Shield className="w-4 h-4" />
          <span>Secure Login • HIPAA Compliant</span>
        </div>
      </div>
    </div>
  );
}