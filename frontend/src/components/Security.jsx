import { useEffect, useState } from "react";
import axios from "axios";

import Navbar from "./Navbar";
import Sidebar from "./Sidebar";


function Security(){


const [alerts,setAlerts] = useState([]);




useEffect(()=>{


const token = localStorage.getItem("token");


axios.get(
"http://127.0.0.1:5000/reports",
{
headers:{
Authorization:`Bearer ${token}`
}
}
)
.then((res)=>{


let data=[];


res.data.forEach((report)=>{


if(report.security_alerts){


report.security_alerts.forEach((alert)=>{


data.push({

file: report.filename,

alert: alert

});


});


}


});


setAlerts(data);


})
.catch((err)=>{

console.log(err);

});


},[]);





return (

<div className="layout">


<Sidebar/>


<div className="main">


<Navbar/>




<div className="security-page">


<h1>
Security Center
</h1>



<div className="security-banner">


<h2>
Threat Detection System
</h2>


<p>
Network traffic security monitoring
</p>


</div>





{

alerts.length === 0 ?


<div className="security-card">


<h3>
No Security Alerts
</h3>


<p>
Your analyzed packets are clean
</p>


</div>


:


alerts.map((item,index)=>(


<div 
className="security-card"
key={index}
>


<div>

<h3>
⚠ Alert Detected
</h3>


<p>
{item.alert}
</p>


</div>



<span>

{item.file}

</span>



</div>


))


}





</div>



</div>


</div>


);


}
export default Security;