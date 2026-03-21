import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  Area,
  AreaChart,
} from "recharts";

const forecastData = [
  { week: "Week 1", predicted: 38, actual: 37, threshold: 60 },
  { week: "Week 2", predicted: 42, actual: 41, threshold: 60 },
  { week: "Week 3", predicted: 45, actual: null, threshold: 60 },
  { week: "Week 4", predicted: 48, actual: null, threshold: 60 },
  { week: "Week 5", predicted: 52, actual: null, threshold: 60 },
  { week: "Week 6", predicted: 55, actual: null, threshold: 60 },
  { week: "Week 7", predicted: 58, actual: null, threshold: 60 },
  { week: "Week 8", predicted: 61, actual: null, threshold: 60 },
];

const nurseBurnoutRisk = [
  { nurse: "NU_1", currentScore: 65, predicted4Weeks: 78, risk: "Critical" },
  { nurse: "NU_4", currentScore: 72, predicted4Weeks: 82, risk: "Critical" },
  { nurse: "HN_9", currentScore: 67, predicted4Weeks: 75, risk: "High" },
  { nurse: "HN_5", currentScore: 55, predicted4Weeks: 68, risk: "High" },
  { nurse: "NU_2", currentScore: 42, predicted4Weeks: 52, risk: "Moderate" },
  { nurse: "HN_7", currentScore: 45, predicted4Weeks: 54, risk: "Moderate" },
];

export function BurnoutForecast() {
  const getRiskColor = (risk: string) => {
    switch (risk) {
      case "Critical":
        return "text-[#DC2626]";
      case "High":
        return "text-[#EF4444]";
      case "Moderate":
        return "text-[#F59E0B]";
      default:
        return "text-[#16A34A]";
    }
  };

  const getRiskBg = (risk: string) => {
    switch (risk) {
      case "Critical":
        return "bg-[#DC2626]/10 border border-[#DC2626]";
      case "High":
        return "bg-[#EF4444]/10 border border-[#EF4444]";
      case "Moderate":
        return "bg-[#F59E0B]/10 border border-[#F59E0B]";
      default:
        return "bg-[#16A34A]/10 border border-[#16A34A]";
    }
  };

  return (
    <div className="p-8 max-w-[1400px] mx-auto">
      {/* Header */}
      <h1 className="text-3xl font-bold text-[#1E293B] mb-8">Burnout Forecast & Risk Analysis</h1>

      {/* Summary Cards */}
      <div className="grid grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-xl p-6 border border-[#E2E8F0]">
          <div className="text-3xl font-bold text-[#1E293B] mb-2">37.9</div>
          <div className="text-sm text-[#64748B]">Current Avg Fatigue</div>
        </div>
        <div className="bg-white rounded-xl p-6 border border-[#E2E8F0]">
          <div className="text-3xl font-bold text-[#DC2626] mb-2">61.2</div>
          <div className="text-sm text-[#64748B]">Predicted (8 weeks)</div>
        </div>
        <div className="bg-white rounded-xl p-6 border border-[#E2E8F0]">
          <div className="text-3xl font-bold text-[#F59E0B] mb-2">6</div>
          <div className="text-sm text-[#64748B]">At-Risk Nurses</div>
        </div>
        <div className="bg-white rounded-xl p-6 border border-[#E2E8F0]">
          <div className="text-3xl font-bold text-[#DC2626] mb-2">2</div>
          <div className="text-sm text-[#64748B]">Critical Cases</div>
        </div>
      </div>

      {/* Forecast Chart */}
      <div className="bg-white rounded-xl p-6 mb-8 border border-[#E2E8F0]">
        <h2 className="text-xl font-bold text-[#1E293B] mb-6">8-Week Burnout Forecast</h2>
        <ResponsiveContainer width="100%" height={400}>
          <AreaChart data={forecastData}>
            <defs>
              <linearGradient id="colorPredicted" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#2563EB" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#2563EB" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
            <XAxis dataKey="week" stroke="#64748B" />
            <YAxis stroke="#64748B" />
            <Tooltip
              contentStyle={{
                backgroundColor: "#FFFFFF",
                border: "1px solid #E2E8F0",
                borderRadius: "8px",
                color: "#1E293B",
              }}
            />
            <Legend />
            <Area
              type="monotone"
              dataKey="predicted"
              stroke="#2563EB"
              strokeWidth={3}
              fill="url(#colorPredicted)"
              name="Predicted Fatigue"
            />
            <Line
              type="monotone"
              dataKey="actual"
              stroke="#16A34A"
              strokeWidth={3}
              dot={{ fill: "#16A34A", r: 5 }}
              name="Actual Fatigue"
            />
            <Line
              type="monotone"
              dataKey="threshold"
              stroke="#F59E0B"
              strokeWidth={2}
              strokeDasharray="5 5"
              name="Risk Threshold"
              dot={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* High-Risk Nurses Table */}
      <div className="bg-white rounded-xl p-6 border border-[#E2E8F0]">
        <h2 className="text-xl font-bold text-[#1E293B] mb-6">High-Risk Nurses</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-[#E2E8F0]">
                <th className="px-6 py-3 text-left text-sm text-[#64748B]">Nurse ID</th>
                <th className="px-6 py-3 text-left text-sm text-[#64748B]">Current Score</th>
                <th className="px-6 py-3 text-left text-sm text-[#64748B]">Predicted (4 weeks)</th>
                <th className="px-6 py-3 text-left text-sm text-[#64748B]">Risk Level</th>
              </tr>
            </thead>
            <tbody>
              {nurseBurnoutRisk.map((nurse, index) => (
                <tr key={index} className="border-b border-[#E2E8F0]">
                  <td className="px-6 py-4 text-[#1E293B]">{nurse.nurse}</td>
                  <td className="px-6 py-4 text-[#1E293B]">{nurse.currentScore}</td>
                  <td className="px-6 py-4 text-[#DC2626]">{nurse.predicted4Weeks}</td>
                  <td className="px-6 py-4">
                    <span
                      className={`px-3 py-1 rounded-full text-sm ${getRiskBg(
                        nurse.risk
                      )} ${getRiskColor(nurse.risk)}`}
                    >
                      {nurse.risk}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}