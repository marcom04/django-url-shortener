import React, { Component } from 'react';
import { Container, Col, Row } from 'react-bootstrap';

import ShortenForm from './ShortenForm';


class Home extends Component {
    render() {
        return (
            <Container style={{ marginTop: "20px" }}>
                <Row>
                    <Col lg={{ span:6, offset:3 }}>
                        <ShortenForm />
                    </Col>
                </Row>
            </Container>
        );
    }
}

export default Home;
