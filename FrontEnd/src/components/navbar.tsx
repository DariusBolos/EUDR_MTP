import '../../node_modules/bootstrap/dist/css/bootstrap.min.css'
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { Link } from 'react-router-dom';

export default function MenuBar() {
    return (
        <div className='navbar-container'>
            <Navbar data-bs-theme="dark">
                <Container>
                    <img src='/osapiens_logo.jpeg' alt="logo" width={80} height={80} />
                    <Nav className="me-auto">
                        <Nav.Link as={Link} to="/">Registration</Nav.Link>
                        <Nav.Link as={Link} to="/dashboard">Dashboard</Nav.Link>
                        <Nav.Link as={Link} to="/admin/weights">Weights</Nav.Link>
                    </Nav>
                </Container>
            </Navbar>
        </div>
    )
}