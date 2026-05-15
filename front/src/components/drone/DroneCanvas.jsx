import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import DroneModel from "./DroneModel";

export default function DroneCanvas({ action }) {
  return (
    <div className="h-full w-full relative bg-cyan-200">
      <Canvas camera={{ position: [5, 3, 5] }}>
        <ambientLight intensity={0.6} />
        <pointLight position={[10, 10, 10]} />

        <DroneModel action={action} />

        <OrbitControls />
      </Canvas>

      <div className="absolute top-2 left-2 bg-black text-white text-xs p-2">
        STATUS: {action || "IDLE"}
      </div>
    </div>
  );
}
