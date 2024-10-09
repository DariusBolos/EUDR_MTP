import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import '../../node_modules/bootstrap/dist/css/bootstrap.min.css'
import { FormEvent, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Commodity from "../interfaces/commodity.ts";
import Country from "../interfaces/country.ts";

export default function RegistrationForm() {
    const [countries, setCountries] = useState<Country[]>([]);
    const [commodities, setCommodities] = useState<Commodity[]>([]);

    const navigate = useNavigate();

    function formSubmission (event: FormEvent) {
        event.preventDefault();

        const form = event.target as HTMLFormElement;

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        console.log(JSON.stringify(data));
        
        fetch('http://localhost:8080/customers', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
    }

    useEffect(() => {
        fetch('http://localhost:8080')
            .then(res => res.json())
            .then(data => {
                const {commodities, countries} = data;
                setCommodities(commodities);
                setCountries(countries);
            })
    }, [])

    return (
        <div className='form-container'>
            <form id='form' method='POST' onSubmit={(e)=> {
                    formSubmission(e);
                    navigate('/dashboard');
                }
            }>
            <Form.Group className="mb-3" controlId="formBasicName">
                <Form.Label>Company Name</Form.Label>
                <Form.Control name="customerName" type="text" placeholder="Please enter the company name" />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicAddress">
                <Form.Label>Address</Form.Label>
                <Form.Control name="customerAddress" type="text" placeholder="Enter the Address of the Company" />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Import Country</Form.Label>
                <Form.Select name="importCountry">
                    <option>Select a country</option>
                    {
                        countries.map((country, index) => (
                            <option key={index} value={country.code}>{country.name}</option>
                        ))
                    }
                </Form.Select>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicRegion">
                <Form.Label>Region</Form.Label>
                <Form.Control name="region" type="text" placeholder="Select the region" />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicZip">
                <Form.Label>Zip Code</Form.Label>
                <Form.Control name="zip" type="text" placeholder="Enter the Zip Code" />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Commodity</Form.Label>
                <Form.Select name="commodity">
                    <option>Select a commodity</option>
                    {
                        commodities.map((commodity, index) => (
                            <option key={index} value={commodity.id}>{commodity.name}</option>
                        ))
                    }
                </Form.Select>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicYear">
                <Form.Label>Year of Trade</Form.Label>
                <Form.Control name="tradeYear" type="number" placeholder="Enter the year of trade" />
            </Form.Group>
            <Button className="submit-button" variant="primary" type="submit">Submit</Button>
            </form>
        </div>
    )
}