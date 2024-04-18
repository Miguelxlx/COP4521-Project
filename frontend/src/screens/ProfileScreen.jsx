import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { Container, Row, Col, Card, Alert } from 'react-bootstrap';

const ProfileScreen = () => {
    const userInfo = useSelector(state => state.auth.userInfo);
    const [profile, setProfile] = useState({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchProfile = async () => {
            if (!userInfo) {
                setError('User not logged in');
                return;
            }
            setLoading(true);
            try {
                const response = await fetch(`http://127.0.0.1:5000/profile?email=${userInfo.email}`);
                const data = await response.json();
                if (response.ok) {
                    setProfile(data);
                } else {
                    throw new Error(data.message || 'Failed to fetch profile data');
                }
            } catch (err) {
                console.error('Fetch error:', err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchProfile();
    }, [userInfo]);

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
                            {profile.name ? (
                                <>
                                    <p><strong>Name:</strong> {profile.name}</p>
                                    <p><strong>Email:</strong> {profile.email}</p>
                                    <p><strong>Balance:</strong> ${profile.balance}</p>
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
