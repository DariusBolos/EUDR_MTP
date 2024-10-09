import RegistrationForm from '../components/form'
import '../css/registration.css'

export default function RegistrationPage() {
    return(
        <div className='registration-page-wrapper'>
            <h1>Registration of Supplier</h1>
            <RegistrationForm />
        </div>
    )
}