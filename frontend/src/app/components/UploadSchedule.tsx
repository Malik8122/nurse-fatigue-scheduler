import { useState, useEffect, useRef } from "react";
import { Upload, CheckCircle2, Play } from "lucide-react";
import { Button } from "./ui/button";
import { Slider } from "./ui/slider";

const API = "http://localhost:8000";

export function UploadSchedule() {
  const [generations,         setGenerations]         = useState([50]);
  const [population,          setPopulation]          = useState([30]);
  const [isScheduleGenerated, setIsScheduleGenerated] = useState(false);
  const [isGenerating,        setIsGenerating]        = useState(false);
  const [stats,               setStats]               = useState<any>(null);
  const [results,             setResults]             = useState<any>(null);
  const [csvFile,             setCsvFile]             = useState<File | null>(null);
  const [csvInfo,             setCsvInfo]             = useState<any>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetch(`${API}/api/dataset-stats`)
      .then(r => r.json())
      .then(setStats)
      .catch(() => {});
  }, []);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setCsvFile(file);
    const form = new FormData();
    form.append("file", file);
    try {
      const res  = await fetch(`${API}/api/upload-csv`, { method: "POST", body: form });
      const data = await res.json();
      setCsvInfo(data);
    } catch {
      alert("Could not connect to API. Make sure uvicorn is running.");
    }
  };

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      const res  = await fetch(`${API}/api/generate-schedule`, {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify({ generations: generations[0], pop_size: population[0] }),
      });
      const data = await res.json();
      setResults(data);
      setIsScheduleGenerated(true);
    } catch {
      alert("Error connecting to API server. Make sure uvicorn is running on port 8000.");
    }
    setIsGenerating(false);
  };

  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold text-[#1E293B] mb-8">Upload Nurse Data & Generate Schedule</h1>

      {/* Dataset Stats */}
      <div className="grid grid-cols-4 gap-6 mb-8">
        {[
          { label: "NSPLib Files",     value: stats?.nsplib_files     ?? "..." },
          { label: "Benchmark-24",     value: stats?.benchmark24      ?? "..." },
          { label: "Benchmark-225",    value: stats?.benchmark225     ?? "..." },
          { label: "Validation Set",   value: stats?.validation_files ?? "..." },
        ].map((s) => (
          <div key={s.label} className="bg-white rounded-xl p-6 shadow-sm border border-[#E2E8F0]">
            <div className="text-3xl font-bold text-[#1E293B] mb-2">{s.value}</div>
            <div className="text-sm text-[#64748B]">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Model Status */}
      <div className={`rounded-xl p-4 mb-8 flex items-center gap-3 border ${
        stats?.model_trained
          ? "bg-[#16A34A]/10 border-[#16A34A]"
          : "bg-yellow-50 border-yellow-400"
      }`}>
        <CheckCircle2 className={`w-5 h-5 ${stats?.model_trained ? "text-[#16A34A]" : "text-yellow-500"}`} />
        <span className={stats?.model_trained ? "text-[#16A34A]" : "text-yellow-700"}>
          {stats?.model_trained ? "Burnout model is trained and ready" : "Model not trained yet"}
        </span>
      </div>

      {/* CSV Upload — fixed file input */}
      <div className="bg-white rounded-xl p-8 mb-8 border border-[#E2E8F0]">
        <h2 className="text-xl font-bold text-[#1E293B] mb-4">Upload Nurse Roster CSV</h2>

        {/* Hidden real file input */}
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          style={{ display: "none" }}
        />

        {/* Clickable upload area */}
        <div
          onClick={() => fileInputRef.current?.click()}
          className="border-2 border-dashed border-[#CBD5E1] rounded-xl p-12 text-center hover:border-[#2563EB] transition-colors cursor-pointer"
        >
          <Upload className="w-12 h-12 text-[#64748B] mx-auto mb-4" />
          <p className="text-[#64748B] mb-4">
            {csvFile ? csvFile.name : "Click here or drag and drop your CSV file"}
          </p>
          <Button
            variant="outline"
            className="border-[#E2E8F0] text-[#1E293B] hover:bg-[#F8FAFC]"
            type="button"
            onClick={(e) => { e.stopPropagation(); fileInputRef.current?.click(); }}
          >
            Browse Files
          </Button>
        </div>

        {csvInfo && (
          <div className="mt-4 p-4 bg-green-50 rounded-lg border border-green-200">
            <p className="text-green-700 font-medium">
              ✓ Loaded {csvInfo.rows} nurses · {csvInfo.columns?.length} columns
            </p>
            <p className="text-green-600 text-sm mt-1">
              Columns: {csvInfo.columns?.slice(0, 5).join(", ")}...
            </p>
          </div>
        )}
      </div>

      {/* GA Panel */}
      <div className="bg-white rounded-xl p-8 border border-[#E2E8F0]">
        <h2 className="text-2xl font-bold text-[#1E293B] mb-6">Generate Optimal Schedule via NSGA-II</h2>

        <div className="space-y-6 mb-8">
          <div>
            <div className="flex justify-between items-center mb-3">
              <label className="text-[#1E293B]">Generations</label>
              <span className="text-[#2563EB] font-bold">{generations[0]}</span>
            </div>
            <Slider value={generations} onValueChange={setGenerations}
              min={10} max={500} step={10}
              className="[&_[role=slider]]:bg-[#2563EB]" />
          </div>
          <div>
            <div className="flex justify-between items-center mb-3">
              <label className="text-[#1E293B]">Population Size</label>
              <span className="text-[#2563EB] font-bold">{population[0]}</span>
            </div>
            <Slider value={population} onValueChange={setPopulation}
              min={20} max={200} step={10}
              className="[&_[role=slider]]:bg-[#2563EB]" />
          </div>
        </div>

        <Button onClick={handleGenerate} disabled={isGenerating}
          className="w-full bg-[#2563EB] hover:bg-[#1D4ED8] text-white py-6 text-lg">
          <Play className="w-5 h-5 mr-2" />
          {isGenerating ? "Running NSGA-II... please wait" : "Generate Optimal Schedule"}
        </Button>

        {isScheduleGenerated && results && (
          <div className="mt-8">
            <div className="bg-[#16A34A]/10 border border-[#16A34A] rounded-xl p-4 mb-6 flex items-center gap-3">
              <CheckCircle2 className="w-5 h-5 text-[#16A34A]" />
              <span className="text-[#16A34A]">Schedule generated successfully!</span>
            </div>
            <div className="grid grid-cols-3 gap-6">
              <div className="bg-[#F8FAFC] rounded-xl p-6 border border-[#E2E8F0]">
                <div className="text-2xl font-bold text-[#1E293B] mb-2">{results.avg_fatigue}/100</div>
                <div className="text-sm text-[#64748B]">Avg Fatigue Score</div>
              </div>
              <div className="bg-[#F8FAFC] rounded-xl p-6 border border-[#E2E8F0]">
                <div className="text-2xl font-bold text-[#DC2626] mb-2">{results.high_risk}</div>
                <div className="text-sm text-[#64748B]">High Risk Nurses</div>
              </div>
              <div className="bg-[#F8FAFC] rounded-xl p-6 border border-[#E2E8F0]">
                <div className="text-2xl font-bold text-[#1E293B] mb-2">{results.total_nurses}</div>
                <div className="text-sm text-[#64748B]">Nurses Scheduled</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}