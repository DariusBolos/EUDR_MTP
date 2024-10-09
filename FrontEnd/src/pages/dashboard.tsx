import '../css/dashboard.css'
import InformationTable from "../components/table";

export default function DashboardPage() {
    return (
        <div className="dashboard-page-wrapper">
            <h1>Dashboard</h1>
            <InformationTable/>
        </div>
    )
}