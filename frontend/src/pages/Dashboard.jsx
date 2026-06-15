import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import StatCard from "../components/StatCard";
import AlertCard from "../components/AlertCard";

import {
  PieChart,
  Pie,
  Tooltip,
  ResponsiveContainer
} from "recharts";



function Dashboard(){


const navigate = useNavigate();


const [reports,setReports] = useState([]);




useEffect(()=>{


const getReports = async()=>{


try{


const token = localStorage.getItem("token");


const res = await axios.get(

"http://127.0.0.1:5000/reports",

{
headers:{
Authorization:`Bearer ${token}`
}
}

);


setReports(res.data);



}

catch(err){

console.log(err);

}



}



getReports();



},[]);





let total = 0;
let tcp = 0;
let udp = 0;
let alertCount = 0;



reports.forEach((r)=>{


total += r.total_packets;

tcp += r.tcp_packets;

udp += r.udp_packets;


if(r.security_alerts){

alertCount += r.security_alerts.length;

}


});





const chartData = [

{
name:"TCP",
value:tcp
},

{
name:"UDP",
value:udp
}

];





return (


<div className="layout">


<Sidebar/>




<div className="main">



<Navbar/>




<div className="dashboard">



<h1>
Network Traffic Dashboard
</h1>





<div className="stats">


<StatCard

title="Reports"

value={reports.length}

type="reports"

/>




<StatCard

title="Packets"

value={total}

type="packets"

/>





<StatCard

title="Alerts"

value={alertCount}

type="alerts"

/>



</div>






<div className="dashboard-grid">





<div className="chart-card">


<h2>
Protocol Distribution
</h2>



<ResponsiveContainer
width="100%"
height={300}
>


<PieChart>


<Pie

data={chartData}

dataKey="value"

cx="50%"

cy="50%"

outerRadius={100}

/>



<Tooltip/>


</PieChart>


</ResponsiveContainer>



</div>







<AlertCard

alerts={
reports[0]?.security_alerts
}

/>




</div>








<div className="report-card">


<h2>
Analysis History
</h2>




<table>


<thead>

<tr>

<th>
File
</th>


<th>
Packets
</th>


<th>
TCP
</th>


<th>
UDP
</th>


</tr>


</thead>





<tbody>


{

reports.map((r)=>(


<tr

key={r.id}

onClick={()=>navigate(`/report/${r.id}`)}

>


<td>
{r.filename}
</td>


<td>
{r.total_packets}
</td>


<td>
{r.tcp_packets}
</td>


<td>
{r.udp_packets}
</td>



</tr>


))


}



</tbody>


</table>




</div>





</div>




</div>



</div>


)



}


export default Dashboard;