import { useEffect,useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/axios";


import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import AlertCard from "../components/AlertCard";



function Report(){



const {id} = useParams();


const [report,setReport] = useState(null);





useEffect(()=>{


const fetchReport = async()=>{


try{


const res = await api.get(`/reports/${id}`);



setReport(res.data);



}

catch(err){

console.log(err);

}



}




fetchReport();



},[id]);






if(!report){


return (

<h2>
Loading Report...
</h2>

)


}






return (



<div className="layout">



<Sidebar/>




<div className="main">



<Navbar/>






<div className="report-page">





<h1>
Traffic Analysis Report
</h1>




<div className="report-card">



<h2>
{report.filename}
</h2>



<p>
Total Packets : {report.total_packets}
</p>


<p>
TCP : {report.tcp_packets}
</p>


<p>
UDP : {report.udp_packets}
</p>


<p>
ICMP : {report.icmp_packets}
</p>




</div>






<AlertCard

alerts={report.security_alerts}

/>





<div className="report-card">



<h2>
Top Source IPs
</h2>



{

report.top_source_ips.map((ip,index)=>(


<p key={index}>

{ip[0]} : {ip[1]}

</p>


))


}



</div>





</div>





</div>



</div>



)



}



export default Report;
