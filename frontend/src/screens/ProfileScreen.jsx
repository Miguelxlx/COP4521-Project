import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { Container, Row, Col, Card, Alert } from 'react-bootstrap';

const ProfileScreen = () => {
    const userInfo = useSelector(state => state.auth.userInfo);
    const [profile, setProfile] = useState({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

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
