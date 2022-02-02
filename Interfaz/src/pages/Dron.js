import * as React from "react";
import * as THREE from "three";
import io from "socket.io-client";
import {useState, useEffect} from "react";

import {SocketContext} from '../context/socket';
import {useContext, useCallback} from 'react';

const Dron = () => {

  const socket = useContext(SocketContext);

  const ref = React.useRef();
  const [loaded, setLoaded] = React.useState(false);
  

  React.useEffect(() => {

    let posx;
    let posy;
    let posz;
    
    socket.on('connect', () => {
        console.log("I'm connected with the back-end");
        socket.on('disconnect', () => {
            console.log('user disconnected');
        });
    });

    // Recibimos los valores por el canal prueba
        socket.on('Datos', (msg) => {
            posy=parseInt((msg).split(',')[1]);
            posx=parseInt((msg).split(',')[2]);
            posz=parseInt((msg).split(',')[3]);
        }); 

    if (!loaded && ref) {
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
      );

      const renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setSize(window.innerWidth -180, window.innerHeight -80);

      const geometry = new THREE.BoxBufferGeometry(2,2,2)//DodecahedronBufferGeometry(1.7, 0);
      const material = new THREE.MeshStandardMaterial({
        color: "#00FFFF"
      });

      const light = new THREE.AmbientLight(0x0ffff);
      light.position.set(30, 30, 30);
      scene.add(light);

      camera.position.z = 5;
      camera.position.x = 1;

      const Figure = new THREE.Mesh(geometry, material);

      scene.add(Figure);

      const animate = () => {
        requestAnimationFrame(animate);
        Figure.rotation.x =posy/100;
        console.log(posx/100)
        Figure.rotation.y = posx/100;
        Figure.rotation.z = posz/100;
        renderer.render(scene, camera);
      };

      const resize = () => {
        renderer.setSize(window.innerWidth, window.innerHeight);
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
      };

      animate();
      ref.current.appendChild(renderer.domElement);
      window.addEventListener("resize", resize);
      setLoaded(true);
      return () => window.removeEventListener("resize", resize);
    }
  }, [ref, loaded]);

  return <div ref={ref} />;
}

/*
<div className="App">
                
                <table>
                    <thead>
                        <tr>
                            <th>Datos recibidos del dron </th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr>
                            <td>Altura: </td>
                            <td>{altura} </td>
                        </tr>
                        <tr>
                            <td>Pitch: </td>
                            <td>{pitch} </td>
                        </tr>
                        <tr>
                            <td>Roll: </td>
                            <td>{roll} </td>
                        </tr>
                        <tr>
                            <td>Yaw: </td>
                            <td>{yaw} </td>
                        </tr>
                    </tbody>
                </table>
            </div>
*/

export default Dron;
