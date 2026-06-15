import {
    FileText,
    Network,
    ShieldAlert
  } from "lucide-react";
  
  
  function StatCard({title,value,type}){
  
  
  const icons = {
  
  reports:<FileText size={30}/>,
  
  packets:<Network size={30}/>,
  
  alerts:<ShieldAlert size={30}/>
  
  };
  
  
  
  return (
  
  <div className="stat-card">
  
  
  
  <div className="stat-icon">
  
  {icons[type]}
  
  </div>
  
  
  
  
  <div className="stat-content">
  
  
  <h3>
  {title}
  </h3>
  
  
  <h1>
  {value}
  </h1>
  
  
  
  </div>
  
  
  
  </div>
  
  )
  
  
  }
  
  
  export default StatCard;