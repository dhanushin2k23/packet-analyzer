import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";


function Login(){


const navigate = useNavigate();


const [email,setEmail] = useState("");
const [password,setPassword] = useState("");

const [error,setError] = useState("");





const handleLogin = async(e)=>{


e.preventDefault();



try{


const res = await api.post(

"/login",

{
email,
password
}

);




localStorage.setItem(

"token",

res.data.access_token

);





navigate("/dashboard");



}

catch(err){


console.log(err);



if(err.response){

setError(
err.response.data.error
);

}

else{

setError(
"Server not responding"
);

}


}



}







return (



<div className="auth-page">



<div className="auth-card">



<h1>
Packet Analyzer
</h1>


<p>
Login to continue
</p>





<form onSubmit={handleLogin}>


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

Login

</button>



</form>







{
error &&

<p className="error">

{error}

</p>

}







<p>

Don't have an account?

</p>



<button

className="secondary-btn"

onClick={()=>navigate("/register")}

>

Register

</button>





</div>



</div>



)


}


export default Login;
