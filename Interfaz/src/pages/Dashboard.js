import {useState, useEffect, useRef} from "react";
import Highcharts from 'highcharts';
import HighchartsReact from "highcharts-react-official";
import {SocketContext} from '../context/socket';
import {useContext, useCallback} from 'react';


const Dashboard = () => {

    const socket = useContext(SocketContext);
    const [response,setResponse] = useState("");
    const [troll,setRoll] = useState() 

    socket.on('connect', () => {
        console.log("I'm connected with the back-end");
        socket.on('disconnect', () => {
            console.log('user disconnected');
        });
    });

    var xroll = [];
    var xyaw = [];
    var xpitch = [];
    var cont = 0;
    useEffect(() =>{
    // Recibimos los valores por el canal prueba
        socket.on('Datos', (msg) => {
            console.log(msg);
            setResponse(msg);
            xroll[cont] = (parseInt(msg.split(",")[2]))
            setOptionsRoll({ series: [{ data: xroll  }] });
            xpitch[cont] = (parseInt(msg.split(",")[1]))
            setOptionsPitch({ series: [{ data: xpitch  }] });
            xyaw[cont] = (parseInt(msg.split(",")[3]))
            setOptionsYaw({ series: [{ data: xyaw  }] });
            cont = cont+1;
            
        }); 
    },[]);

    var datosRecibidos = response.split(",");
    var altura = datosRecibidos[0];
    var pitch = datosRecibidos[1];
    var roll = datosRecibidos[2];
    var yaw = datosRecibidos[3];
    

    const [optionsRoll,setOptionsRoll] = useState( {
        
        chart: {
            type: 'spline',
            showAxes: true,
            width: 430
        },
        title: {
            text: 'Roll'
        },
        yAxis: {
            min: -91,
            max: 91,
        },
         series: [{
            name: 'Roll',
            data: [], 
         }]
    });

    const [optionsYaw,setOptionsYaw] = useState( {
        
        chart: {
            type: 'spline',
            showAxes: true,
            width: 430
        },
        title: {
            text: 'Yaw'
        },
        yAxis: {
            min: -91,
            max: 91,
        },
         series: [{
            name: 'Yaw',
            data: [], 
         }]
    });

    const [optionsPitch,setOptionsPitch] = useState( {
        
        chart: {
            type: 'spline',
            showAxes: true,
            width: 430
        },
        title: {
            text: 'Pitch'
        },
        yAxis: {
            min: -91,
            max: 91,
        },
         series: [{
            name: 'Pitch',
            data: [], 
         }]
    });

    return(
        <div>
            <br></br>
            <div className="d-flex flex-row">
            <div>
                <HighchartsReact
                    allowChartUpdate={true}
                    highcharts={Highcharts}
                    options={optionsRoll}
                />
            </div>
            <div>
                <HighchartsReact
                    allowChartUpdate={true}
                    highcharts={Highcharts}
                    options={optionsPitch}
                />
            </div>
            <div>
                <HighchartsReact
                    allowChartUpdate={true}
                    highcharts={Highcharts}
                    options={optionsYaw}
                />
            </div> 
        </div>
        </div>
        
    )
}

export default Dashboard;