import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Container, Row, Col, Card, Alert, Button, Form } from 'react-bootstrap';
import { setCredentials } from '../slices/authSlice';

const ProfileScreen = () => {
    const userInfo = useSelector(state => state.auth.userInfo);
    const dispatch = useDispatch();  // Use dispatch if you're updating the redux store

    const [profile, setProfile] = useState({});
    const [loading, setLoading] = useState(false);

    const [error, setError] = useState('');
    const [amount, setAmount] = useState(0);  // State to store the amount to be added

    //const [updateUserBalance, { isLoading }] = useUpdateUserBalanceMutation()
    const handleAddBalance = async () => {
        if (!amount || amount <= 0) {
            setError('Please enter a valid amount.');
            return;
        }
        setLoading(true)
        const newBalance = parseFloat(userInfo.balance) + parseFloat(amount);
        try {
            const response = await fetch('http://127.0.0.1:5000/update_balance', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id: userInfo.id,
                    newBalance: newBalance
                }),
            });
            const data = await response.json();
            if (response.ok) {
                dispatch(setCredentials(data.user));
                console.log(data.user)
                console.log("Balance updated successfully")
                setError('');
                alert('Balance updated successfully!');
            } else {
                //const errorData = await response.json();
                setError(data.message);
            }
        } catch (err) {
            setError(err);
        } finally {
            setLoading(false);
        }
    };
    

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <Alert variant="danger">{error}</Alert>;
    }

    return (
        <Container>
            <Row className="justify-content-md-center">
                <Col xl={12} md={6}>
                    <Card>
                        <Card.Header>Profile Information</Card.Header>
                        <Card.Body>
                            {userInfo ? (
                                <>
                                    <p><strong>Name:</strong> {userInfo.username}</p>
                                    <p><strong>Email:</strong> {userInfo.email}</p>
                                    <p><strong>Balance:</strong> ${userInfo.balance}</p>
                                    <Form>
                                        <Form.Group>
                                            <Form.Label>Add to Balance:</Form.Label>
                                            <Form.Control
                                                type="number"
                                                placeholder="Enter amount"
                                                value={amount}
                                                onChange={(e) => setAmount(e.target.value)}
                                            />
                                        </Form.Group>
                                        <Button variant="primary" onClick={handleAddBalance}>
                                            Add Balance
                                        </Button>
                                    </Form>
                                </>
                            ) : (
                                <p>No profile data available.</p>
                            )}
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
    );
};

export default ProfileScreen;
