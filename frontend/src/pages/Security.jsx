import {useEffect,useState} from "react";
import api from "../api/axios";


function Security(){


const [reports,setReports]=useState([]);




useEffect(()=>{


const load=async()=>{


const res=await api.get("/reports");



setReports(res.data);



};


load();


},[]);




return (

<div className="dashboard">


<h1>
Security
</h1>



{
reports.length===0

?

<div className="card">

No alerts

</div>


:


reports.map((r)=>(


<div 
className="card"
key={r.id}
>


<h3>
{r.filename}
</h3>


<p>
Security analysis completed
</p>


</div>


))


}



</div>


);


}


export default Security;
