import React, { useRef } from 'react';
import EarthDayMap from '../textures/earth_daymap.jpeg';
import EarthNormalMap from '../textures/earth_normal_map.jpeg';
import EarthSpecularMap from '../textures/earth_specular_map.jpeg';
import EarthNightMap from '../textures/earth_nightmap.jpeg';
import EarthCloudsMap from '../textures/earth_clouds.jpeg';
import { TextureLoader, geLight } from 'three';
import { useFrame, useLoader } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import * as THREE from 'three';

export function Earth(props) { // Generate normal_map from user's classification data
    const [colorMap, normalMap, specularMap, cloudMap] = useLoader(TextureLoader, [EarthDayMap, EarthNormalMap, EarthSpecularMap, EarthCloudsMap]);
    /*const specularMap = new THREE TextureLoader().load(EarthSpecularMap); -> Does THREE need to be imported explicitly on a next base?
    const colorMap = new TextureLoader().load(EarthDayMap); -> Generate texture maps from perlin noise & replace normalMap
    const normalMap = new TextureLoader().load(EarthNormalMap); -> Just have these values be passed in via an API call, then generate a video and share it with the client (for the first iteration?)
    We've got an issue here -> TextureLoad syntax not working on Next.js build...we have to switch back to React to continue bootstrapping until we can figure out what's going on. Until then, iFrame or API call between this app and main Next to get it rendering on main signal-k/client app? Render it with react-scripts but still on Next? Have it as a single page app that's manually rendered in?*/

    const earthRef = useRef();
    const cloudsRef = useRef();
    useFrame(({ clock }) => { // Executed each frame
        const elapsedTime = clock.getElapsedTime();
        earthRef.current.rotation.y = elapsedTime / 6;
        cloudsRef.current.rotation.y = elapsedTime / 6;
    });

    return (
        <>
            <pointLight color="#f6f3ea" position={[2, 0, 5]} intensity={1.2} /> {/* Make the colour of the sun slightly yellowed, by the earth's atmosphere */}
            <Stars radius={300} depth={60} count={20000} factor={7} saturation={0} fade={true} />
            <mesh ref={cloudsRef}>
                <sphereGeometry args={[1.005, 32, 32]} />
                <meshPhongMaterial map={cloudMap} opacity={0.4} depthWrite={true} transparent={true} side={THREE.DoubleSide} />
            </mesh>
            <mesh ref={earthRef}>
                <sphereGeometry args={[1, 32, 32]} />
                <meshPhongMaterial specularMap={specularMap} />
                <meshStandardMaterial map={colorMap} normalMap={normalMap} metalness={0.7} />
                <OrbitControls enableZoom={true} enablePan={true} enableRotate={true} zoomSpeed={0.6} panSpeed={0.5} rotateSpeed={0.4} />
            </mesh>
        </>
    )
}