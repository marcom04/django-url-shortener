import React from 'react';
import { Container, Form, Button, InputGroup, Toast } from 'react-bootstrap';
import { format } from 'date-fns';
import axios from 'axios';

import { GUEST_SHORTEN_API_URL } from '../constants';

class ShortenForm extends React.Component {
    state = {
        target: "",
        short_url: "",
        shorten_disabled: false,
        short_url_hidden: true,
        expiry_date: new Date(),
        showCopied: false
    };

    toggleShowCopied = () => this.setState({showCopied: !this.state.showCopied});

    copyToClipboard = () => {
        navigator.clipboard.writeText(this.state.short_url).then(() => {
            this.toggleShowCopied();
        });
    }

    onChange = e => {
        this.setState({ [e.target.name]: e.target.value });
    };

    resetState = () => {
        this.setState({
            target: "",
            short_url: "",
            shorten_disabled: false,
            short_url_hidden: true,
            expiry_date: new Date()
        });
    };

    createMapping = e => {
        e.preventDefault();
        axios.post(GUEST_SHORTEN_API_URL, {target: this.state.target}).then(response => {
            this.setState({
               short_url: response.data.short_url,
               expiry_date: new Date(response.data.expiry_date),
               shorten_disabled: true,
               short_url_hidden: false
           });
        }).catch(err => {
            console.log(err);
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
                            required
                            placeholder="Enter the URL to shorten..."
                            value={this.state.target}
                            onChange={this.onChange}
                        />
                    </Form.Group>
                    <Form.Group className="mb-3" hidden={this.state.short_url_hidden}>
                        <Form.Label htmlFor="short_url">
                            Here's your shortened URL, valid until: {format(this.state.expiry_date, 'yyyy/MM/dd HH:mm')}
                        </Form.Label>
                        <InputGroup className="mb-3">
                            <Form.Control
                                name="short_url"
                                type="text"
                                readOnly
                                value={this.state.short_url}
                            />
                            <Button
                                onClick={this.copyToClipboard}
                                variant="outline-secondary"
                            >
                              Copy
                            </Button>
                            <Button
                                href={this.state.short_url}
                                variant="outline-secondary"
                                target="_blank"
                            >
                              Visit
                            </Button>
                        </InputGroup>

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

                <Toast show={this.state.showCopied} onClose={this.toggleShowCopied}>
                    <Toast.Header>
                        <span className="me-auto">Copied to clipboard!</span>
                    </Toast.Header>
                </Toast>
            </Container>
        );
    }
}

export default ShortenForm;
