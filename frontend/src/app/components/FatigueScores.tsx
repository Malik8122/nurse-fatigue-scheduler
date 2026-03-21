import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine, Cell } from "recharts";

const API = "http://localhost:8000";

const getColor = (score: number) => score >= 60 ? "#DC2626" : score >= 30 ? "#F59E0B" : "#16A34A";

export function FatigueScores() {
  const [data,    setData]    = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/api/fatigue`)
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-[#64748B]">Loading fatigue scores...</div>;
  if (!data || data.error)
    return <div className="p-8 text-[#64748B]">No schedule yet. Go to Upload page and generate one first.</div>;

  const chartData = [...data.nurses].sort((a: any, b: any) => b.score - a.score);

  return (
    <div className="p-8 max-w-[1400px] mx-auto">
      <h1 className="text-3xl font-bold text-[#1E293B] mb-8">Nurse Fatigue Scores</h1>

      {/* Summary Cards */}
      <div className="grid grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-xl p-6 border border-[#E2E8F0]">
          <div className="text-3xl font-bold text-[#DC2626] mb-2">{data.high}</div>
          <div className="text-sm text-[#1E293B] mb-1">High Risk</div>
          <div className="text-xs text-[#64748B]">60–100 score</div>
        </div>
        <div className="bg-white rounded-xl p-6 border border-[#E2E8F0]">
          <div className="text-3xl font-bold text-[#F59E0B] mb-2">{data.moderate}</div>
          <div className="text-sm text-[#1E293B] mb-1">Moderate Risk</div>
          <div className="text-xs text-[#64748B]">30–60 score</div>
        </div>
        <div className="bg-white rounded-xl p-6 border border-[#E2E8F0]">
          <div className="text-3xl font-bold text-[#16A34A] mb-2">{data.low}</div>
          <div className="text-sm text-[#1E293B] mb-1">Low Risk</div>
          <div className="text-xs text-[#64748B]">0–30 score</div>
        </div>
      </div>

      {/* Bar Chart */}
      <div className="bg-white rounded-xl p-6 mb-8 border border-[#E2E8F0]">
        <h2 className="text-xl font-bold text-[#1E293B] mb-6">Fatigue Score per Nurse</h2>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="nurse" stroke="#64748B" />
            <YAxis stroke="#64748B" />
            <Tooltip contentStyle={{ backgroundColor: "#FFFFFF", border: "1px solid #E2E8F0", borderRadius: "8px" }} />
            <ReferenceLine y={60} stroke="#DC2626" strokeDasharray="3 3"
              label={{ value: "High Risk (NHS)", fill: "#DC2626", position: "right" }} />
            <ReferenceLine y={30} stroke="#F59E0B" strokeDasharray="3 3"
              label={{ value: "Moderate", fill: "#F59E0B", position: "right" }} />
            <Bar dataKey="score" radius={[8, 8, 0, 0]}>
              {chartData.map((entry: any, index: number) => (
                <Cell key={index} fill={getColor(entry.score)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Legend */}
      <div className="bg-white rounded-xl p-6 border border-[#E2E8F0]">
        <h3 className="text-lg font-bold text-[#1E293B] mb-4">Risk Level Legend</h3>
        <div className="flex gap-8">
          {[["#DC2626","High Risk (60-100)"],["#F59E0B","Moderate Risk (30-60)"],["#16A34A","Low Risk (0-30)"]].map(([color, label]) => (
            <div key={label} className="flex items-center gap-3">
              <div className="w-4 h-4 rounded" style={{ background: color }}></div>
              <span className="text-[#64748B]">{label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}