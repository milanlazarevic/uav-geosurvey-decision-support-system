import { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

export default function DroneModel({ action }) {
  const groupRef = useRef();
  const bodyRef = useRef();
  const arrowRef = useRef();
  const warningRef = useRef();
  const rotorRefs = useRef([]);

  const state = useRef({
    pos: new THREE.Vector3(0, 0, 0),
    rotation: 0,
  });

  useFrame((stateObj, delta) => {
    if (!groupRef.current || !bodyRef.current) return;

    const time = stateObj.clock.getElapsedTime();

    // Reset visibility
    if (arrowRef.current) arrowRef.current.visible = false;
    if (warningRef.current) warningRef.current.visible = false;

    // Simple animations based on action
    switch (action) {
      case "CONTINUE":
        // Move forward slowly
        state.current.pos.x = Math.sin(time * 0.5) * 1.5;
        bodyRef.current.rotation.z = Math.sin(time * 2) * 0.05; // Gentle tilt
        if (arrowRef.current) {
          arrowRef.current.visible = true;
          arrowRef.current.rotation.y = 0;
          arrowRef.current.rotation.z = -Math.PI / 2;
          arrowRef.current.material.opacity = 0.8 + Math.sin(time * 3) * 0.2;
        }
        break;

      case "RETURN_TO_HOME":
        // Rotate and show return arrow
        state.current.rotation = Math.sin(time * 1.5) * Math.PI * 0.2;
        if (arrowRef.current) {
          arrowRef.current.visible = true;
          arrowRef.current.rotation.y = 0;
          arrowRef.current.rotation.z = Math.PI / 2; // Point backward
          arrowRef.current.material.opacity = 0.8 + Math.sin(time * 3) * 0.2;
        }
        break;

      case "LAND":
        // Move down slowly
        state.current.pos.y = -Math.abs(Math.sin(time * 0.8)) * 0.8;
        bodyRef.current.rotation.z = 0;
        if (arrowRef.current) {
          arrowRef.current.visible = true;
          arrowRef.current.rotation.y = 0;
          arrowRef.current.rotation.z = Math.PI; // Point down
          arrowRef.current.material.opacity = 0.8 + Math.sin(time * 3) * 0.2;
        }
        break;

      case "SLOW_DOWN": {
        const scale = 1 + Math.sin(time * 4) * 0.08;

        // ?. safely checks if the ref and scale exist before setting
        bodyRef.current?.scale.set(scale, scale, scale);

        if (warningRef.current) {
          warningRef.current.visible = true;
          warningRef.current.rotation.y = time * 2;

          // Check if it's a mesh with a material, or traverse if it's a group
          if (warningRef.current.material) {
            warningRef.current.material.transparent = true;
            warningRef.current.material.opacity =
              0.6 + Math.sin(time * 5) * 0.4;
          } else {
            // If it's a group/model, apply to all parts
            warningRef.current.traverse((child) => {
              if (child.isMesh) {
                child.material.transparent = true;
                child.material.opacity = 0.6 + Math.sin(time * 5) * 0.4;
              }
            });
          }
        }
        break;
      }

      default:
        break;
    }

    // Spin rotors
    rotorRefs.current.forEach((rotor) => {
      if (rotor) {
        rotor.rotation.y += delta * 25;
      }
    });

    groupRef.current.position.copy(state.current.pos);
    groupRef.current.rotation.y = state.current.rotation;
  });

  return (
    <group ref={groupRef}>
      <group ref={bodyRef}>
        {/* Simple drone body - flat minimalist style */}
        <mesh position={[0, 0, 0]}>
          <boxGeometry args={[0.5, 0.12, 0.5]} />
          <meshStandardMaterial color="#34495e" />
        </mesh>

        {/* Four rotors - spinning discs */}
        {[
          [0.35, 0.35],
          [-0.35, 0.35],
          [0.35, -0.35],
          [-0.35, -0.35],
        ].map((pos, idx) => (
          <group key={idx} position={[pos[0], 0.1, pos[1]]}>
            {/* Rotor arm */}
            <mesh position={[0, -0.05, 0]}>
              <cylinderGeometry args={[0.02, 0.02, 0.1, 8]} />
              <meshStandardMaterial color="#7f8c8d" />
            </mesh>
            {/* Rotor blade */}
            <mesh ref={(el) => (rotorRefs.current[idx] = el)}>
              <cylinderGeometry args={[0.18, 0.18, 0.02, 16]} />
              <meshStandardMaterial color="#3498db" opacity={0.6} transparent />
            </mesh>
          </group>
        ))}

        {/* Action Arrow - points in direction of movement */}
        <mesh
          ref={arrowRef}
          position={[0.8, 0, 0]}
          visible={false}
          rotation={[0, 0, -Math.PI / 2]}
        >
          <coneGeometry args={[0.25, 0.6, 3]} />
          <meshStandardMaterial
            color={
              action === "CONTINUE"
                ? "#27ae60"
                : action === "RETURN_TO_HOME"
                  ? "#f39c12"
                  : "#3498db"
            }
            transparent
            opacity={0.9}
            emissive={
              action === "CONTINUE"
                ? "#27ae60"
                : action === "RETURN_TO_HOME"
                  ? "#f39c12"
                  : "#3498db"
            }
            emissiveIntensity={0.3}
          />
        </mesh>

        {/* Warning Icon for SLOW_DOWN */}
        <group ref={warningRef} position={[0, 0.5, 0]} visible={false}>
          {/* Triangle background */}
          <mesh rotation={[0, 0, 0]}>
            <cylinderGeometry args={[0.3, 0.3, 0.05, 3]} />
            <meshStandardMaterial
              color="#e74c3c"
              transparent
              opacity={0.95}
              emissive="#e74c3c"
              emissiveIntensity={0.4}
            />
          </mesh>
          {/* Exclamation line */}
          <mesh position={[0, 0.05, 0.03]}>
            <boxGeometry args={[0.1, 0.28, 0.02]} />
            <meshStandardMaterial color="#ffffff" />
          </mesh>
          {/* Exclamation dot */}
          <mesh position={[0, -0.15, 0.03]}>
            <boxGeometry args={[0.1, 0.1, 0.02]} />
            <meshStandardMaterial color="#ffffff" />
          </mesh>
        </group>
      </group>

      {/* Colored glow based on action */}
      <pointLight
        position={[0, 0.5, 0]}
        color={
          action === "CONTINUE"
            ? "#27ae60"
            : action === "RETURN_TO_HOME"
              ? "#f39c12"
              : action === "LAND"
                ? "#3498db"
                : "#e74c3c"
        }
        intensity={2}
        distance={4}
      />
    </group>
  );
}
