import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";


function Register(){


const navigate = useNavigate();



const [username,setUsername] = useState("");
const [email,setEmail] = useState("");
const [password,setPassword] = useState("");

const [message,setMessage] = useState("");





const handleRegister = async(e)=>{


e.preventDefault();




try{


await axios.post(

"http://127.0.0.1:5000/register",

{
username,
email,
password
}

);




setMessage(
"Account created successfully"
);




setTimeout(()=>{

navigate("/");

},1000);




}

catch(err){


console.log(err);



if(err.response){

setMessage(
err.response.data.error
);

}

else{

setMessage(
"Server error"
);

}


}



}








return (



<div className="auth-page">



<div className="auth-card">





<h1>
Create Account
</h1>



<p>
Network Traffic Analyzer
</p>






<form onSubmit={handleRegister}>


<input

type="text"

placeholder="Username"

value={username}

onChange={(e)=>setUsername(e.target.value)}

required

/>







<input

type="email"

placeholder="Email"

value={email}

onChange={(e)=>setEmail(e.target.value)}

required

/>







<input

type="password"

placeholder="Password"

value={password}

onChange={(e)=>setPassword(e.target.value)}

required

/>








<button type="submit">

Register

</button>





</form>







{
message &&

<p>

{message}

</p>

}








<button

className="secondary-btn"

onClick={()=>navigate("/")}

>

Already have account? Login

</button>





</div>



</div>



)


}



export default Register;