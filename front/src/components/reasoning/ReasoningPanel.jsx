export default function ReasoningPanel({ data }) {
  if (!data) return null;

  const { decision, warnings, facts, gnss, battery, signal, speed } = data;

  return (
    <div className="flex flex-col h-full bg-slate-950 font-mono">
      {/* HEADER */}
      <div className="p-4 border-b border-slate-800 bg-slate-900/50 flex justify-between items-center">
        <h2 className="text-xs font-black tracking-widest text-cyan-500 uppercase">
          System Reasoning Panel
        </h2>
        <span className="text-[10px] text-slate-500">LIVE_STATE_v3</span>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-6 custom-scrollbar">
        {/* ================= DECISION ================= */}
        {decision && (
          <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-xl">
            <div className="text-[10px] text-red-400 uppercase mb-2">
              FINAL DECISION
            </div>

            <div className="text-2xl font-black text-white uppercase">
              {decision.action}
            </div>

            <div className="text-xs text-slate-300 mt-1">
              State: <span className="text-red-400">{decision.state}</span>
            </div>

            <p className="text-xs text-slate-400 mt-2">{decision.reason}</p>

            <div className="text-[10px] text-slate-500 mt-2">
              {new Date(decision.timestamp).toLocaleString()}
            </div>
          </div>
        )}

        {/* ================= WARNINGS ================= */}
        <div>
          <h3 className="text-[10px] text-yellow-400 mb-2 uppercase">
            Warnings
          </h3>

          <div className="space-y-2">
            {warnings
              ?.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
              .map((w, i) => (
                <div
                  key={i}
                  className="p-2 bg-yellow-500/10 border border-yellow-500/20 rounded"
                >
                  <p className="text-xs text-yellow-200">{w.message}</p>
                  <p className="text-[10px] text-slate-500">
                    {new Date(w.timestamp).toLocaleString()}
                  </p>
                </div>
              ))}
          </div>
        </div>

        {/* ================= FACTS ================= */}
        <div>
          <h3 className="text-[10px] text-cyan-400 mb-2 uppercase">
            Facts Engine Output
          </h3>

          <div className="flex flex-wrap gap-2">
            {facts?.map((f, i) => (
              <span
                key={i}
                className="text-[10px] px-2 py-1 rounded bg-slate-800 border border-slate-700 text-slate-300"
              >
                {f.value}
              </span>
            ))}
          </div>
        </div>

        {/* ================= TELEMETRY ================= */}
        <div>
          <h3 className="text-[10px] text-emerald-400 mb-2 uppercase">
            Raw Telemetry
          </h3>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <div className="p-3 bg-slate-900 border border-slate-800 rounded">
              <div className="text-slate-500 text-[10px]">GNSS</div>
              <div className="text-white">HDOP: {gnss?.hdop}</div>
              <div className="text-slate-400 text-[10px]">
                SATS: {gnss?.satellites} | {gnss?.fixType}
              </div>
            </div>

            <div className="p-3 bg-slate-900 border border-slate-800 rounded">
              <div className="text-slate-500 text-[10px]">BATTERY</div>
              <div className="text-white">{battery?.level}%</div>
            </div>

            <div className="p-3 bg-slate-900 border border-slate-800 rounded">
              <div className="text-slate-500 text-[10px]">SIGNAL</div>
              <div className="text-white">{signal?.strength}</div>
            </div>

            <div className="p-3 bg-slate-900 border border-slate-800 rounded">
              <div className="text-slate-500 text-[10px]">SPEED</div>
              <div className="text-white">{speed?.speed} m/s</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
