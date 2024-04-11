import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { useRegisterMutation } from '../slices/usersApiSlice';
import { Form, Button, Row, Col } from 'react-bootstrap';

const RegisterScreen = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [message, setMessage] = useState(null);

    const navigate = useNavigate();

    const submitHandler = async (e) => {
        e.preventDefault();
        if (password !== confirmPassword) {
            setMessage('Passwords do not match');
        } else {
            const userData = {
                name: name,
                email: email,
                password: password
            };
    
            try {
                const response = await fetch("http://127.0.0.1:5000/register", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(userData)
                });
    
                if (response.ok) {
                    const data = await response.json();
                    if (data.valid === true){
                        setMessage('Registration successful');
                        navigate('/')
                    }
                    else{
                        setMessage('Email already in use');
                    }
                } else {
                    setMessage('Email already in use');
                    throw new Error('Failed to register');
                }
            } catch (err) {
                console.error('Failed to register: ', err);
            }
        }
    };
    

    return (
        <Row className="justify-content-md-center">
            <Col xl={12} md={6}>
                <h1>Sign Up</h1>
                {message && <div className="alert alert-danger">{message}</div>}
                <Form onSubmit={submitHandler}>
                    <Form.Group controlId='name'>
                        <Form.Label>Name</Form.Label>
                        <Form.Control
                            type='name'
                            placeholder='Enter name'
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                        ></Form.Control>
                    </Form.Group>

                    <Form.Group controlId='email'>
                        <Form.Label>Email Address</Form.Label>
                        <Form.Control
                            type='email'
                            placeholder='Enter email'
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        ></Form.Control>
                    </Form.Group>

                    <Form.Group controlId='password'>
                        <Form.Label>Password</Form.Label>
                        <Form.Control
                            type='password'
                            placeholder='Enter password'
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        ></Form.Control>
                    </Form.Group>

                    <Form.Group controlId='confirmPassword'>
                        <Form.Label>Confirm Password</Form.Label>
                        <Form.Control
                            type='password'
                            placeholder='Confirm password'
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                        ></Form.Control>
                    </Form.Group>

                    <Button type='submit' variant='primary'>
                        Register
                    </Button>
                </Form>

                <Row className="py-3">
                    <Col>
                        Have an Account? <Link to={'/login'}>Login</Link>
                    </Col>
                </Row>
            </Col>
        </Row>
    );
};

export default RegisterScreen;