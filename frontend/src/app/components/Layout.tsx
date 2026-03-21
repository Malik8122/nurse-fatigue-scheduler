import { Outlet, Link, useLocation } from "react-router";
import { Upload, Calendar, Activity, TrendingUp, LogOut } from "lucide-react";

export function Layout() {
  const location = useLocation();

  const navItems = [
    { path: "/dashboard", label: "Upload & Schedule", icon: Upload },
    { path: "/dashboard/schedule", label: "Schedule View", icon: Calendar },
    { path: "/dashboard/fatigue", label: "Fatigue Scores", icon: Activity },
    { path: "/dashboard/burnout", label: "Burnout Forecast", icon: TrendingUp },
  ];

  return (
    <div className="flex h-screen bg-[#F8FAFC]">
      {/* Sidebar */}
      <div className="w-60 bg-[#1E3A8A] flex flex-col">
        {/* App Title */}
        <div className="p-6 border-b border-[#1E40AF]">
          <h1 className="text-xl font-bold text-white">Hospital Scheduler AI</h1>
        </div>

        {/* Navigation */}
        <nav className="flex-1 py-6">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-6 py-3 transition-colors ${
                  isActive
                    ? "bg-[#2563EB] text-white"
                    : "text-[#BFDBFE] hover:bg-[#1E40AF] hover:text-white"
                }`}
              >
                <Icon className="w-5 h-5" />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* User Section */}
        <div className="p-6 border-t border-[#1E40AF]">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-white">Admin</p>
              <p className="text-xs text-[#93C5FD]">admin@hospital.ai</p>
            </div>
            <button className="p-2 hover:bg-[#1E40AF] rounded-lg transition-colors">
              <LogOut className="w-4 h-4 text-[#BFDBFE]" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <Outlet />
      </div>
    </div>
  );
}