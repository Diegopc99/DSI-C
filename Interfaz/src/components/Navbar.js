import {Navbar,Nav,Container} from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

const NavBar = () => {
    return (
        
        <>
        <Navbar bg="dark" variant="dark" className='navbar' fixed="top">
            <Container>
            <Navbar.Brand>ROOM PILOT</Navbar.Brand>  
            </Container>
        </Navbar>
        </>
    
    )
}

export default NavBar;