import React, { Component } from 'react';
import * as THREE from 'three';
import { MTLoader, OBJLoader } from 'three-obj-mtl-loader'
import { OrbitControls } from '@react-three/drei';

class ThreeScene extends Component { // https://hiteshkrsahu.medium.com/three-js-scene-as-a-react-component-c83cc00f8a4a
    componentDidMount() {
        const width = this.mount.clientWidth;
        const height = this.mount.clientHeight;
        this.scene = new THREE.Scene();

        // Add scene renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setClearColor("#263238");
        this.renderer.setSize(width, height);
        this.mount.appendChild(this.renderer.domElement);

        // Add scene camera
        this.camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
        this.camera.position.z = 8;
        this.camera.position.y = 5;
        const controls = new OrbitControls(this.camera, this.renderer.domElement); // Controls for camera
        
        // Setting up lights
        var lights = [];
        lights[0] = new THREE.PointLight(0x304ffe, 1, 0);
        lights[1] = new THREE.PointLight(0xffffff, 1, 0);
        lights[2] = new THREE.PointLight(0xffffff, 1, 0);
        lights[0].position.set(0, 200, 0);
        lights[1].position.set(100, 200, 100);
        lights[2].position.set(-100, -200, -100);
        this.scene.add(lights[0]);
        this.scene.add(lights[1]);
        this.scene.add(lights[2]);

        // 3D Models

        this.renderScene();

        this.start(); // Start animation
    }

    start = () => {
        if (!this.frameId) {
            this.frameId = requestAnimationFrame(this.animate);
        }
    };

    stop = () => {
        cancelAnimationFrame(this.frameId);
    };

    animate = () => {
        this.renderScene();
        this.frameId = window.requestAnimationFrame(this.animate);
    };
      
    renderScene = () => {
        if (this.renderer) this.renderer.render(this.scene, this.camera);
    }

    render() {
        return (
            <div 
                style={{ width: "800px", height: "800px" }}
                ref={mount => { this.mount = mount}}
            />
        )
    }
}

export default ThreeScene;