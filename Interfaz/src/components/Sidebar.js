import React from "react";
import {Nav} from "react-bootstrap";
import 'bootstrap/dist/css/bootstrap.min.css'
import '../App.css'
import 'react-minimal-side-navigation/lib/ReactMinimalSideNavigation.css';
import {Navigation} from 'react-minimal-side-navigation';
import { useHistory } from 'react-router-dom';

const Sidebar = () => {

  let history = useHistory();

  function Handleroute(itemId){
    history.push(itemId);
  }
   
    return (
        <>
        <Navigation
            // you can use your own router's api to get pathname
            activeItemId="/home"
            onSelect={({itemId}) => {
              // maybe push to the route
              Handleroute(itemId)
            }}
            
            // items //
            items={[
              {
                title: 'Home',
                itemId: '/home',
              },
              {
                title: 'Dashboard',
                itemId: '/dashboard',
              },
              {
                title: 'Control PID',
                itemId: '/control',
              },
              // {
              //   title:'Dron',
              //   itemId:'/dron'
              // },
              {
                title: 'Mapa',
                itemId: '/mapa',
              }
            ]}
          />
            
        </>
        );
    };
    //const Sidebar = withRouter(Side);
    export default Sidebar