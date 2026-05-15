export default function TelemetrySliders({ telemetry, setTelemetry }) {
  const handleChange = (key, val) => {
    setTelemetry((prev) => ({ ...prev, [key]: Number(val) }));
  };

  return (
    <div className="p-6 bg-slate-900/80 backdrop-blur-md border border-slate-700 rounded-2xl shadow-2xl w-full max-w-md">
      <div className="flex items-center gap-2 mb-6">
        <div className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
        <h4 className="text-xs font-black tracking-widest text-cyan-400 uppercase">
          Drone Systems Telemetry
        </h4>
      </div>

      <div className="space-y-6">
        {Object.entries(telemetry).map(([key, value]) => (
          <div key={key} className="group">
            {/* Header: Label + Live Value */}
            <div className="flex justify-between items-end mb-2">
              <label className="text-[10px] font-bold text-slate-400 uppercase tracking-tighter group-hover:text-cyan-300 transition-colors">
                {key.replace(/([A-Z])/g, " $1")}
              </label>
              <span className="font-mono text-sm text-cyan-400 bg-cyan-950/50 px-2 py-0.5 rounded border border-cyan-800/50">
                {value}
              </span>
            </div>

            {/* Range Slider */}
            <div className="relative flex items-center">
              <input
                type="range"
                min="0"
                max="100"
                step="0.1"
                value={value}
                onChange={(e) => handleChange(key, e.target.value)}
                className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-500 hover:accent-cyan-400 transition-all"
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
