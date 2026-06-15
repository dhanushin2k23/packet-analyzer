import { ShieldAlert } from "lucide-react";


function AlertCard({alerts}){


if(!alerts || alerts.length === 0){

return (

<div className="alert-card">

<ShieldAlert/>

<h3>
No Security Alerts
</h3>


<p>
No suspicious activity detected
</p>


</div>

)

}



return (

<div className="alert-card">


<div className="alert-header">


<ShieldAlert size={28}/>


<h3>
Security Alerts
</h3>


</div>




{

alerts.map(

(alert,index)=>(


<div
className="alert-item"
key={index}
>


<p>
⚠️ {alert}
</p>


</div>


)

)


}



</div>

)


}


export default AlertCard;