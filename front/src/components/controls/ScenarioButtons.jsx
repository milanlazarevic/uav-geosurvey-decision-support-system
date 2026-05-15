export default function ScenarioButtons({ run }) {
  const scenarios = [
    {
      id: "battery",
      label: "Battery Drain",
      color: "hover:bg-red-500/20 hover:border-red-500",
      text: "text-red-400",
      icon: "⚡",
    },
    {
      id: "signal",
      label: "Degrade Signal",
      color: "hover:bg-orange-500/20 hover:border-orange-500",
      text: "text-orange-400",
      icon: "📡",
    },
    {
      id: "speed",
      label: "High Speed",
      color: "hover:bg-emerald-500/20 hover:border-emerald-500",
      text: "text-emerald-400",
      icon: "🚀",
    },
    {
      id: "gnss",
      label: "Poor GNSS",
      color: "hover:bg-yellow-500/20 hover:border-yellow-500",
      text: "text-yellow-400",
      icon: "🛰️",
    },
  ];

  return (
    <div className="p-4 bg-slate-900/90 border border-slate-700 rounded-xl shadow-xl">
      <h3 className="text-[10px] font-bold text-slate-300 uppercase tracking-[0.2em] mb-4 flex items-center">
        <span className="w-1.5 h-1.5 bg-red-600 rounded-full mr-2 animate-pulse" />
        Fault Injection System
      </h3>

      <div className="grid grid-cols-2 gap-3">
        {scenarios.map((s) => (
          <button
            key={s.id}
            onClick={() => run(s.id)}
            className={`
              relative overflow-hidden group
              flex flex-col items-start p-3 
              bg-slate-800/40 border border-slate-700/50 
              rounded-lg transition-all duration-200
              active:scale-95 active:bg-slate-700
              ${s.color}
            `}
          >
            {/* Background Accent Decor */}
            <div className="absolute top-0 right-0 p-1 opacity-10 group-hover:opacity-30 transition-opacity">
              <span className="text-2xl">{s.icon}</span>
            </div>

            <span
              className={`text-[10px] font-black uppercase tracking-tighter mb-1 ${s.text}`}
            >
              Scenario_{s.id}
            </span>
            <span className="text-xs font-medium text-slate-200">
              {s.label}
            </span>

            {/* Bottom "Loading" bar decoration */}
            <div className="absolute bottom-0 left-0 h-[2px] w-0 bg-current transition-all duration-500 group-hover:w-full opacity-50" />
          </button>
        ))}
      </div>
    </div>
  );
}
