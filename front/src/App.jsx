import { useSimulation } from "./hooks/useSimulation";

import DashboardLayout from "./components/layout/DashboardLayout";
import ControlPanel from "./components/controls/ControlPanel";
import DroneCanvas from "./components/drone/DroneCanvas";
import ReasoningPanel from "./components/reasoning/ReasoningPanel";
import { useEffect, useState } from "react";
import { connect, disconnect } from "./api/wsclient";

export default function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    connect(setData);
    return () => disconnect();
  }, []);

  console.log(data);
  const sim = useSimulation();

  const runScenario = async (type) => {
    const delay = (ms) => new Promise((r) => setTimeout(r, ms));

    if (type === "battery") {
      await sim.send({ battery: 30 });
      await delay(1000);
      await sim.send({ battery: 5 });
    }

    if (type === "signal") {
      await sim.send({ signal: 40 });
      await delay(1000);
      await sim.send({ signal: 15 });
    }

    if (type === "speed") {
      await sim.send({ speed: 180 });
    }

    if (type === "gnss") {
      await sim.send({ satellites: 2, hdop: 8 });
    }
  };
  // console.log(sim.decision);
  return (
    <DashboardLayout
      left={
        <ControlPanel
          telemetry={sim.telemetry}
          setTelemetry={sim.setTelemetry}
          send={sim.send}
          reset={sim.reset}
          runScenario={runScenario}
        />
      }
      center={<DroneCanvas action={data?.decision?.action} />}
      right={<ReasoningPanel data={data} />}
    />
  );
}
