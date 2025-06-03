import React, { useRef, useEffect } from "react";
import { Canvas, useFrame, useLoader } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";

function Head({ state }) {
  const group = useRef();
  const gltf = useLoader(GLTFLoader, "/models/head_avatar.glb");

  useEffect(() => {
    if (!gltf.scene) return;
    const sceneClone = gltf.scene.clone(true);
    const headOnlyGroup = new THREE.Group();
    headOnlyGroup.name = "HeadOnlyGroup";

    const keepNames = ["Wolf3D_Head", "EyeLeft", "EyeRight", "Wolf3D_Hair", "Wolf3D_Teeth"];

    sceneClone.traverse((child) => {
      if (child.isMesh && keepNames.includes(child.name)) {
        headOnlyGroup.add(child.clone());
      }
    });

    // Increase scale to fill container
    headOnlyGroup.scale.set(15, 15, 15);
    headOnlyGroup.position.set(0, 0, 0);

    if (group.current) {
      group.current.clear();
      group.current.add(headOnlyGroup);
    }
  }, [gltf]);

  useFrame(() => {
    if (!group.current) return;
    let targetY = 0;
    let targetX = 0;

    switch (state) {
      case "listening":
        targetY = Math.sin(Date.now() / 500) * 0.2;
        break;
      case "speaking":
        targetX = Math.sin(Date.now() / 300) * 0.2;
        break;
      case "happy":
        targetY = 0.5;
        break;
      case "sad":
        targetY = -0.5;
        break;
      default:
        targetY = 0;
        targetX = 0;
    }

    group.current.rotation.y += (targetY - group.current.rotation.y) * 0.1;
    group.current.rotation.x += (targetX - group.current.rotation.x) * 0.1;
  });

  return <group ref={group} />;
}

export default function Avatar3D({ state = "idle" }) {
  return (
    <Canvas orthographic camera={{ zoom: 250, position: [0, 0, 5] }} style={{ width: "100%", height: "100%" }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 5, 5]} intensity={1} />
      <Head state={state} />
      <OrbitControls enableZoom={false} enablePan={false} enableRotate={false} />
    </Canvas>
  );
}
