import NavBar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Mapa from './pages/Mapa';
import Dron from './pages/Dron';
import Home from './components/Home';
import ControlPID from './pages/ControlPID';

import {BrowserRouter as Router, Redirect, Route } from "react-router-dom"
import {SocketContext, socket} from './context/socket';

function App() {

  return (
    <SocketContext.Provider value={socket}>
    <Router>
    <div className="container">
      <div className="navbar">
        <NavBar />
      </div>
      <div className="contentANDsidebar">
        <div className="sidebar">
          <Sidebar />
        </div>
        <div className="content">
          <Route path="/dashboard" exact={true} component={Dashboard}/>
          <Route path="/mapa" exact={true} component={Mapa}/>
          <Route path="/dron" exact={true} component={Dron}/>
          <Route path="/home" exact={true} component={Home}/>
          <Route path="/control" exact={true} component={ControlPID}/>
        </div>
      </div>
      </div>
    </Router>
    </SocketContext.Provider>
  );
}

export default App;
