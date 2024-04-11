import { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Form, Button, Row, Col, Modal } from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import FormContainer from '../components/FormContainer';
import Loader from '../components/Loader';
import { setCredentials } from '../slices/authSlice';

const LoginScreen = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [modalMessage, setModalMessage] = useState('');

    const navigate = useNavigate();
    const dispatch = useDispatch();

    const userInfo = useSelector(state => state.auth.userInfo);

    const location = useLocation();
    const redirect = new URLSearchParams(location.search).get('redirect') || '/';

    useEffect(() => {
        if (userInfo) {
            navigate(redirect);
        }
    }, [userInfo, redirect, navigate]);

    const handleCloseModal = () => setShowModal(false);

    const handleLogin = async (e) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            const response = await fetch('http://127.0.0.1:5000/check_login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();
            if (response.ok) {
                setModalMessage('Login successful');
                setShowModal(true);
                dispatch(setCredentials(data));  // Assuming setCredentials will set the user info and auth tokens in the Redux store
                setTimeout(() => {
                    handleCloseModal();
                    navigate(redirect);
                }, 2000);
            } else {
                setModalMessage(data.message || 'Login failed');
                setShowModal(true);
            }
        } catch (error) {
            console.error('Login error:', error);
            setModalMessage('An error occurred during login');
            setShowModal(true);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: '100vh',
            flexDirection: 'column'
        }}>
            <FormContainer>
                <h1>Sign In</h1>
                <Form onSubmit={handleLogin}>
                    <Form.Group controlId='email' className="my-3">
                        <Form.Label>Email Address</Form.Label>
                        <Form.Control
                            type='email'
                            placeholder='Enter email'
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </Form.Group>

                    <Form.Group controlId='password' className="my-3">
                        <Form.Label>Password</Form.Label>
                        <Form.Control
                            type='password'
                            placeholder='Enter password'
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </Form.Group>

                    <Button type='submit' variant='primary' className="mt-2" disabled={isLoading}>
                        Sign In
                    </Button>
                    {isLoading && <Loader />}
                </Form>

                <Row className='py-3'>
                    <Col>
                        New User? <Link to={redirect ? `/register?redirect=${redirect}` : '/register'}>Register</Link>
                    </Col>
                </Row>
            </FormContainer>

            <Modal show={showModal} onHide={handleCloseModal}>
                <Modal.Header closeButton>
                    <Modal.Title>Login Status</Modal.Title>
                </Modal.Header>
                <Modal.Body>{modalMessage}</Modal.Body>
            </Modal>
        </div>
    );
};

export default LoginScreen;
