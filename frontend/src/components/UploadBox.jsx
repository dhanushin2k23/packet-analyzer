import { useState } from "react";
import api from "../api/axios";

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


const res = await api.post(

"/upload",

formData
);



setMessage(
"Analysis completed successfully"
);



console.log(res.data);



}

catch(err){


console.log(err);

const serverMessage = err.response?.data?.details || err.response?.data?.error || err.response?.data?.msg;

setMessage(
serverMessage || "Upload failed. Check backend deployment and try again."
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

accept=".pcap,.pcapng"

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
