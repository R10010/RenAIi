import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

interface Avatar3DProps {
  blendshapeWeights: number[];
  emotion: string;
  gestureSequence?: number[][];
}

const Avatar3D: React.FC<Avatar3DProps> = ({ blendshapeWeights, emotion, gestureSequence }) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene>();
  const cameraRef = useRef<THREE.PerspectiveCamera>();
  const rendererRef = useRef<THREE.WebGLRenderer>();
  const faceMeshRef = useRef<THREE.Mesh>();

  useEffect(() => {
    // Initialize scene
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    
    renderer.setSize(300, 300);
    mountRef.current?.appendChild(renderer.domElement);
    
    // Create a simple sphere as placeholder face
    const geometry = new THREE.SphereGeometry(1, 64, 64);
    const material = new THREE.MeshStandardMaterial({ color: 0xffb6c1 });
    const face = new THREE.Mesh(geometry, material);
    scene.add(face);
    
    // Add lights
    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(0, 1, 2);
    scene.add(light);
    
    camera.position.z = 3;
    
    sceneRef.current = scene;
    cameraRef.current = camera;
    rendererRef.current = renderer;
    faceMeshRef.current = face;
    
    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      
      // Simple morph based on blendshape weights (just scale for demo)
      if (faceMeshRef.current && blendshapeWeights) {
        // For demo, scale based on first blendshape (jaw_open)
        faceMeshRef.current.scale.y = 1 + blendshapeWeights[0] * 0.2;
      }
      
      renderer.render(scene, camera);
    };
    
    animate();
    
    return () => {
      mountRef.current?.removeChild(renderer.domElement);
    };
  }, []);
  
  useEffect(() => {
    // Update expression when blendshape weights change
    console.log(`Emotion: ${emotion}`, blendshapeWeights);
  }, [blendshapeWeights, emotion]);
  
  return <div ref={mountRef} className="avatar-3d" />;
};

export default Avatar3D;