import { useState } from "react";
import axios from "axios";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

import {
  UploadCloud,
  FileCheck
} from "lucide-react";



function Upload(){


const [file,setFile] = useState(null);

const [message,setMessage] = useState("");

const [loading,setLoading] = useState(false);





const uploadFile = async()=>{


if(!file){

setMessage(
"Please select a PCAP file"
);

return;

}




const formData = new FormData();


formData.append(
"file",
file
);





try{


setLoading(true);



const token = localStorage.getItem("token");



const res = await axios.post(

"http://127.0.0.1:5000/upload",

formData,

{

headers:{

Authorization:
`Bearer ${token}`,

"Content-Type":
"multipart/form-data"

}

}

);




setMessage(
"PCAP analyzed successfully"
);



console.log(res.data);



}

catch(err){


console.log(err);


if(err.response?.status===401){

setMessage(
"Session expired. Login again"
);

}

else{

setMessage(
"Upload failed"
);

}



}



finally{

setLoading(false);

}



}






return (


<div className="layout">



<Sidebar/>




<div className="main">



<Navbar/>





<div className="upload-page">






<div className="upload-card">



<UploadCloud size={60}/>




<h1>
Upload PCAP File
</h1>



<p>
Upload network capture file for traffic analysis
</p>





<input

type="file"

accept=".pcap"

onChange={(e)=>
setFile(e.target.files[0])
}

/>






{

file &&

<div className="file-info">


<FileCheck size={20}/>


<span>
{file.name}
</span>


</div>


}







<button

onClick={uploadFile}

disabled={loading}

>


{

loading ?

"Analyzing..."

:

"Analyze Traffic"

}



</button>





<h3>
{message}
</h3>





</div>





</div>





</div>



</div>


)


}



export default Upload;