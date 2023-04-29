import React from 'react';
import { Container, Form, Button } from 'react-bootstrap';
import axios from 'axios';

import { GUEST_SHORTEN_API_URL } from '../constants';

class ShortenForm extends React.Component {
    state = {
        target: "",
        short_url: "",
        shorten_disabled: false,
        short_url_hidden: true
    };

    onChange = e => {
        this.setState({ [e.target.name]: e.target.value });
    };

    resetState = () => {
        this.setState({
            target: "",
            short_url: "",
            shorten_disabled: false,
            short_url_hidden: true
        });
    };

    createMapping = e => {
        e.preventDefault();
        axios.post(GUEST_SHORTEN_API_URL, {target: this.state.target}).then(response => {
           this.setState({
               short_url: response.data.short_url,
               shorten_disabled: true,
               short_url_hidden: false
           });
        });
    };

    render() {
        return (
            <Container>
                <Form onSubmit={this.createMapping}>
                    <Form.Group className="mb-3">
                        <Form.Label htmlFor="target">Target URL</Form.Label>
                        <Form.Control
                            name="target"
                            type="url"
                            placeholder="Enter the URL to shorten..."
                            value={this.state.target}
                            onChange={this.onChange}
                        />
                    </Form.Group>
                    <Form.Group className="mb-3" hidden={this.state.short_url_hidden}>
                        <Form.Label htmlFor="short_url">Shortened URL</Form.Label>
                        <Form.Control
                            name="short_url"
                            type="text"
                            disabled
                            value={this.state.short_url}
                        />
                    </Form.Group>
                    <Button
                        variant="primary"
                        type="submit"
                        disabled={this.state.shorten_disabled}
                    >
                        Shorten
                    </Button>
                    <Button
                        className="mx-2"
                        variant="secondary"
                        type="button"
                        onClick={this.resetState}
                    >
                        Reset
                    </Button>
                </Form>
            </Container>
        );
    }
}

export default ShortenForm;
