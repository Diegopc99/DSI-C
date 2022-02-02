import io from "socket.io-client";
import {SocketContext} from '../context/socket';
import { useState } from "react";
import { useContext } from "react";
import './ControlPID.css'

const ControlPID = () => {

        const socket = useContext(SocketContext);

        const [kp_pitch,setKp_pitch] = useState(Number);
        const [ki_pitch,setKi_pitch] = useState(Number);
        const [kd_pitch,setKd_pitch] = useState(Number);
		const [wg_pitch, setWg_pitch] = useState(Number);

        const [kp_roll,setKp_roll] = useState(Number);
        const [ki_roll,setKi_roll] = useState(Number);
        const [kd_roll,setKd_roll] = useState(Number);
		const [wg_roll, setWg_roll] = useState(Number);

        const [kp_yaw,setKp_yaw] = useState(Number);
        const [ki_yaw,setKi_yaw] = useState(Number);
        const [kd_yaw,setKd_yaw] = useState(Number);
		const [wg_yaw, setWg_yaw] = useState(Number);


        socket.on('connect', () => {
                console.log("I'm connected with the back-end");
                socket.on('disconnect', () => {
                    console.log('user disconnected');
                });
        });

        const handleSubmit_pitch = e => {
                e.preventDefault()
                //if (kp) {
                        socket.emit("kp_pitch",kp_pitch);
                //}
                //if (ki) {
                        socket.emit("ki_pitch",ki_pitch);
                //}
                //if (kd) {
                        socket.emit("kd_pitch",kd_pitch);
                //}
			socket.emit("wg_pitch", wg_pitch);
                        socket.emit("update_pitch","update_pitch");
	}
	const handleSubmit_roll = e => {
		e.preventDefault()
		//if(kp) {

                        socket.emit("kp_roll",kp_roll);
                //}
                //if (ki) {
                        socket.emit("ki_roll",ki_roll);
                //}
                //if (kd) {
                        socket.emit("kd_roll",kd_roll);
                //}
			socket.emit("wg_roll", wg_roll);
                        socket.emit("update_roll","update_roll");
	}
	const handleSubmit_yaw = e => {
		e.preventDefault()
                        socket.emit("kp_yaw",kp_yaw);
                //}
                //if (ki) {
                        socket.emit("ki_yaw",ki_yaw);
                //}
                //if (kd) {
                        socket.emit("kd_yaw",kd_yaw);
                //}
			socket.emit("wg_yaw", wg_yaw);
                        socket.emit("update_yaw","update_yaw");

        }
        socket.emit("Datos", "funciona?");

        return (
		<div id="parent">

			<div id="roll">
				<h2>Roll</h2>
				<form onSubmit={handleSubmit_roll}>
				<label>
	                                <span class="param">Kp_roll:</span>
	                                <input type="float" value="0.3" onChange={e => {
	                                                                console.log(e.target.value);
	                                                                if (e.target.value != ""){
	                                                                        setKp_roll(e.target.value)}
	                                                                else {
	                                                                        setKp_roll(0)
	                                                                }}}/>
	                        </label>
	                        <label>
	                                <span class="param">Ki_roll:</span>
	                                <input type="float" value="0.7" onChange={e => {
	                                                                console.log(e.target.value);
	                                                                if (e.target.value != ""){ 
	                                                                        setKi_roll(e.target.value)}
	                                                                else { 
	                                                                        setKi_roll(0)
	                                                                }}}/>
	                        </label>
	                        <label>
	                                <span class="param">Kd_roll:</span>
	                                <input type="float" value="0.3" onChange={e => {
	                                                                console.log(e.target.value);
	                                                                if (e.target.value != ""){ 
	                                                                        setKd_roll(e.target.value)}
	                                                                else { 
	                                                                        setKd_roll(0)
	                                                                }}}/>
	                        </label>
							<label>
									<span class="param">Wg_roll:</span>
									<input type="float" value="2" onChange={e => {
													console.log(e.target.value);
													if (e.target.value != ""){
														setWg_roll(e.target.value)}
													else {
														setWg_yaw(0)
													}}}/>
							</label>
								<br></br>
								<label>
									<input type="submit" value="Submit"/>
								</label>
						</form>
			</div>

			<div id="pitch">
	                        <h2>Pitch</h2>
	                        <form onSubmit={handleSubmit_pitch}>
	                        	<label>
	                            		<span class="param" >Kp_pitch:</span>
	                            		<input type="float" value="0.3" onChange={e => {
	                                                                console.log(e.target.value);
	                                                                if (e.target.value != "") {
	                                                                        setKp_pitch(e.target.value)}
	                                                                else {
                                                                        setKp_pitch(0)  
	                                                                }}}/>
	                        	</label>
	                        	<label>
	                            		<span class="param">Ki_pitch:</span>
 	                               		<input type="float" value="0.7" onChange={e => {
	                                                                console.log(e.target.value);
	                                                                if (e.target.value != "") {
                                                                        	setKi_pitch(e.target.value)}
	                                                                else {
	                                                                        setKi_pitch(0)
	                                                                }}}/>
	                        	</label>
	                        	<label>
	                                	<span class="param">Kd_pitch:</span>
	                                	<input type="float" value="0.3" onChange={e => {
	                                                                console.log(e.target.value);
	                                                                if (e.target.value != "") {
	                                                                	setKd_pitch(e.target.value)}
	                                                                else {
	                                                                        setKd_pitch(0)
	                                                                }}}/>
	                        	</label>
								<label>
										<span class="param">Wg_pitch:</span>
										<input type="float" value="2" onChange={e => {
												console.log(e.target.value);
												if (e.target.value != ""){
												setWg_pitch(e.target.value)}
												else {
													setWg_pitch(0)
												}}}/>
								</label>
								<br></br>
								<label>
									<input type="submit" value="Submit"/>
								</label>
        	                </form>

			</div>

			<div id="yaw">
							<h2>Yaw</h2>
	                        <form onSubmit={handleSubmit_yaw}>
	                        <label>
	                                <span class="param">Kp_yaw:</span>
	                                <input type="float" value="0.2" onChange={e => {
	                                                                console.log(e.target.value);
	                                                                if (e.target.value != ""){
	                                                                        setKp_yaw(e.target.value)}
	                                                                else {

	                                                                        setKp_yaw(0)
	                                                                }}}/>
	                        </label>
	                        <label>
	                                <span class="param">Ki_yaw:</span>
	                                <input type="float" value="0.7" onChange={e => {
	                                                                console.log(e.target.value);
	                                                                if (e.target.value != ""){ 
	                                                                        setKi_yaw(e.target.value)}
	                                                                else { 
	                                                                        setKi_yaw(0)
	                                                                }}}/>
	                        </label>
	                        <label>
	                                <span class="param">Kd_yaw:</span>
	                                <input type="float" value="0.3" onChange={e => {
	                                                                console.log(e.target.value);
	                                                                if (e.target.value != ""){ 
	                                                                        setKd_yaw(e.target.value)}
	                                                                else { 
	                                                                        setKd_yaw(0)
	                                                                }}}/>
	                        </label>
							<label>
									<span class="param">Wg_yaw:</span> 
									<input type="float" value="2" onChange={e => {
										console.log(e.target.value);
										if (e.target.value != ""){
											setWg_yaw(e.target.value)}
										else {
											setWg_yaw(0)
										}}}/>
							</label>
								<br></br>
							<label>
								<input type="submit" value="Submit"/>
							</label>
						</form>
			</div>
	</div>
        )

        }
export default ControlPID;


