import { useState, useEffect } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const API = "http://localhost:8000";

const getCellColor = (shift: string) => {
  switch (shift) {
    case "Early":  return "bg-blue-100 text-blue-700 border-blue-200";
    case "Day":    return "bg-green-100 text-green-700 border-green-200";
    case "Late":   return "bg-purple-100 text-purple-700 border-purple-200";
    case "Night":  return "bg-indigo-100 text-indigo-700 border-indigo-200";
    default:       return "bg-gray-100 text-gray-600 border-gray-200";
  }
};

export function ScheduleView() {
  const [scheduleData,   setScheduleData]   = useState<any>(null);
  const [activeFilters,  setActiveFilters]  = useState<string[]>([]);
  const [loading,        setLoading]        = useState(true);

  useEffect(() => {
    fetch(`${API}/api/schedule`)
      .then(r => r.json())
      .then(data => { setScheduleData(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-[#64748B]">Loading schedule...</div>;
  if (!scheduleData || scheduleData.error)
    return <div className="p-8 text-[#64748B]">No schedule yet. Go to Upload page and generate one first.</div>;

  // Build pivot: nurse -> day -> shift
  const pivot: Record<string, Record<string, string>> = {};
  const allDays: string[] = [];
  for (const row of scheduleData.schedule) {
    if (!pivot[row.nurse]) pivot[row.nurse] = {};
    pivot[row.nurse][row.day] = row.shift;
    if (!allDays.includes(row.day)) allDays.push(row.day);
  }
  const nurses     = Object.keys(pivot);
  const week1Days  = allDays.filter(d => d.startsWith("W1"));

  // Shift distribution
  const shiftCounts: Record<string, number> = {};
  for (const row of scheduleData.schedule) {
    shiftCounts[row.shift] = (shiftCounts[row.shift] || 0) + 1;
  }
  const distData = Object.entries(shiftCounts).map(([shift, count]) => ({ shift, count }));

  const toggleFilter = (n: string) =>
    setActiveFilters(prev => prev.includes(n) ? prev.filter(x => x !== n) : [...prev, n]);

  const filtered = activeFilters.length === 0 ? nurses : nurses.filter(n => activeFilters.includes(n));

  return (
    <div className="p-8 max-w-[1400px] mx-auto">
      <h1 className="text-3xl font-bold text-[#1E293B] mb-8">Shift Schedule Calendar</h1>

      {/* Filter buttons */}
      <div className="mb-8 flex gap-2 flex-wrap">
        {nurses.slice(0, 15).map(n => (
          <button key={n} onClick={() => toggleFilter(n)}
            className={`px-4 py-2 rounded-full transition-colors border text-sm ${
              activeFilters.includes(n)
                ? "bg-[#2563EB] text-white border-[#2563EB]"
                : "bg-white text-[#64748B] border-[#E2E8F0] hover:border-[#2563EB]"
            }`}>
            {n}
          </button>
        ))}
      </div>

      {/* Schedule Table */}
      <div className="bg-white rounded-xl overflow-hidden mb-8 border border-[#E2E8F0]">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-[#F8FAFC]">
                <th className="px-6 py-4 text-left text-sm text-[#1E293B] border-b border-[#E2E8F0]">Nurse</th>
                {week1Days.map(d => (
                  <th key={d} className="px-4 py-4 text-center text-sm text-[#1E293B] border-b border-[#E2E8F0]">{d}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.map((nurse, idx) => (
                <tr key={nurse} className={idx % 2 === 0 ? "bg-white" : "bg-[#F8FAFC]"}>
                  <td className="px-6 py-4 text-[#1E293B] font-medium border-b border-[#E2E8F0]">{nurse}</td>
                  {week1Days.map(d => (
                    <td key={d} className="px-4 py-4 border-b border-[#E2E8F0] text-center">
                      <span className={`px-3 py-1 rounded text-xs inline-block border ${getCellColor(pivot[nurse]?.[d] ?? "Off")}`}>
                        {pivot[nurse]?.[d] ?? "Off"}
                      </span>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Shift Distribution Chart */}
      <div className="bg-white rounded-xl p-6 mb-8 border border-[#E2E8F0]">
        <h2 className="text-xl font-bold text-[#1E293B] mb-6">Shift Distribution</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={distData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="shift" stroke="#64748B" />
            <YAxis stroke="#64748B" />
            <Tooltip contentStyle={{ backgroundColor: "#FFFFFF", border: "1px solid #E2E8F0", borderRadius: "8px" }} />
            <Bar dataKey="count" fill="#2563EB" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Violations */}
      <div className="bg-white rounded-xl p-6 border border-[#E2E8F0]">
        <h2 className="text-xl font-bold text-[#1E293B] mb-6">Constraint Violations</h2>
        {scheduleData.violations?.length === 0 ? (
          <p className="text-[#16A34A]">No constraint violations found!</p>
        ) : (
          <table className="w-full">
            <thead>
              <tr className="border-b border-[#E2E8F0]">
                <th className="px-6 py-3 text-left text-sm text-[#64748B]">Nurse</th>
                <th className="px-6 py-3 text-left text-sm text-[#64748B]">Issue</th>
                <th className="px-6 py-3 text-left text-sm text-[#64748B]">Day</th>
              </tr>
            </thead>
            <tbody>
              {scheduleData.violations?.map((v: any, i: number) => (
                <tr key={i} className="border-b border-[#E2E8F0]">
                  <td className="px-6 py-4 text-[#1E293B]">{v.nurse}</td>
                  <td className="px-6 py-4 text-[#DC2626]">{v.issue}</td>
                  <td className="px-6 py-4 text-[#64748B]">{v.day}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}