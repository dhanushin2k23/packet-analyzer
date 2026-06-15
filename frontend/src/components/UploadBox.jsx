import { useState } from "react";
import axios from "axios";

import {
  UploadCloud,
  FileCheck
} from "lucide-react";


function UploadBox(){


const [file,setFile] = useState(null);

const [message,setMessage] = useState("");




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
"Analysis completed successfully"
);



console.log(res.data);



}

catch(err){


console.log(err);


setMessage(
"Upload failed"
);


}



}





return (


<div className="upload-box">



<UploadCloud size={45}/>



<h2>
Upload PCAP File
</h2>



<input

type="file"

accept=".pcap"

onChange={(e)=>
setFile(e.target.files[0])
}

/>





{

file &&

<p>

<FileCheck size={18}/>

{file.name}

</p>

}





<button

onClick={uploadFile}

>

Analyze Traffic

</button>




<h3>
{message}
</h3>



</div>


)


}


export default UploadBox;