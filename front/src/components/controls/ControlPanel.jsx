import ScenarioButtons from "./ScenarioButtons";
import TelemetrySliders from "./TelemetrySliders";

export default function ControlPanel({
  telemetry,
  setTelemetry,
  send,
  reset,
  runScenario,
}) {
  return (
    <div className="flex flex-col h-screen w-80 bg-slate-950 border-r border-slate-800 shadow-2xl overflow-y-auto custom-scrollbar">
      {/* HEADER */}
      {/* <div className="p-6 border-b border-slate-800 bg-slate-900/30">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-black tracking-tighter text-white italic">
            Controler<span className="text-cyan-500 text-2xl">.</span>
          </h2>
          <div className="px-2 py-1 rounded bg-emerald-500/10 border border-emerald-500/20">
            <span className="text-[10px] font-mono text-emerald-400 animate-pulse">
              ● LIVE_LINK
            </span>
          </div>
        </div>
      </div> */}

      <div className="p-4 space-y-8 flex-1">
        {/* SECTION 1: SCENARIOS */}
        <section>
          <div className="flex items-center gap-2 mb-3 px-1">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">
              Simulation
            </span>
            <div className="flex-1 h-px bg-slate-800" />
          </div>
          <ScenarioButtons run={runScenario} />
        </section>

        {/* SECTION 2: TELEMETRY */}
        <section>
          <div className="flex items-center gap-2 mb-3 px-1">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">
              Telemetry
            </span>
            <div className="flex-1 h-px bg-slate-800" />
          </div>
          <TelemetrySliders telemetry={telemetry} setTelemetry={setTelemetry} />
        </section>
      </div>

      {/* FOOTER ACTIONS */}
      <div className="p-6 bg-slate-900/50 backdrop-blur-lg border-t border-slate-800 space-y-3">
        <button
          onClick={() => send()}
          className="w-full py-4 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold uppercase  rounded-xl transition-all shadow-[0_0_20px_rgba(6,182,212,0.3)] active:scale-95 flex justify-center items-center gap-2"
        >
          <span>Send</span>
          <svg
            className="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2.5"
              d="M14 5l7 7m0 0l-7 7m7-7H3"
            />
          </svg>
        </button>

        <button
          onClick={reset}
          className="w-full py-2 bg-transparent hover:bg-slate-800 text-slate-400 hover:text-white font-bold text-xs uppercase tracking-widest rounded-lg transition-colors border border-slate-700"
        >
          Reset
        </button>
      </div>
    </div>
  );
}
