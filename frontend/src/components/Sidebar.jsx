import { useNavigate } from "react-router-dom";

import {
  LayoutDashboard,
  Upload,
  FileText,
  ShieldAlert
} from "lucide-react";


function Sidebar(){


const navigate = useNavigate();



return (

<div className="sidebar">



<h2>
Analyzer
</h2>




<div
className="menu-item"
onClick={()=>navigate("/dashboard")}
>

<LayoutDashboard size={20}/>

Dashboard

</div>





<div
className="menu-item"
onClick={()=>navigate("/upload")}
>

<Upload size={20}/>

Upload PCAP

</div>





<div
className="menu-item"
onClick={()=>navigate("/report/1")}
>

<FileText size={20}/>

Reports

</div>





<div
className="menu-item"
onClick={()=>navigate("/security")}
>

<ShieldAlert size={20}/>

Security

</div>





</div>

)

}


export default Sidebar;