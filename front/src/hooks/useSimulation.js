import { useCallback, useState } from "react";
import { sendStep, resetSession } from "../api/client";
import { getSessionId } from "../utils/session";

const defaultTelemetry = {
  battery: 100,
  signal: 90,
  speed: 10,
  // satellites: 12,
  // hdop: 1,
  // fixType: "FIX_3D",
};

export function useSimulation() {
  const [sessionId] = useState(getSessionId());
  const [telemetry, setTelemetry] = useState(defaultTelemetry);
  const [decision, setDecision] = useState({ action: "LAND" });
  const [steps, setSteps] = useState([]);
  const [loading, setLoading] = useState(false);

  const send = useCallback(
    async (override = {}) => {
      setLoading(true);
      try {
        const body = { ...telemetry, ...override };

        const res = await sendStep(sessionId, body);

        setDecision(res.data.decision);
        setSteps((prev) => [...res.data.reasoningSteps, ...prev]);
      } finally {
        setLoading(false);
      }
    },
    [telemetry, sessionId],
  );

  const reset = useCallback(async () => {
    await resetSession(sessionId);
    setTelemetry(defaultTelemetry);
    setDecision(null);
    setSteps([]);
  }, [sessionId]);

  return {
    telemetry,
    setTelemetry,
    decision,
    steps,
    send,
    reset,
    loading,
  };
}
