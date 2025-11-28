import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useState, useContext } from "react";
import UploadService from "@/app/services/FileUploadService";
import IFile from "@/app/types/File";
import {Button} from "@/components/ui/button"
import "@/components/loading"
import { Progress } from "@/components/ui/progress"
import useWebSocket, { ReadyState } from 'react-use-websocket';
import { useRouter } from 'next/navigation'
import { Toaster, toast } from "sonner";
import { useEffect } from "react";
import Loading from "@/components/loading";
import Cookies from 'js-cookie'
import { Card } from "./ui/card";
import { Checkbox } from "@/components/ui/checkbox"
import { DropAi } from "./DropAi";
import { DropMod } from "./DropMod";
import http from "@/app/http-common"
import { createContext } from "react";
type discard = {
  disc: boolean
  setDisc: React.Dispatch<React.SetStateAction<boolean>>
    
}

const Discard = createContext<discard | undefined>(undefined);
export function InputFile(props:any) {

  const router = useRouter()
  const [currentFile, setCurrentFile] = useState<File>();
  const [currentFile1, setCurrentFile1] = useState<File>();
  const [progress, setProgress] = useState<number>(0);
  const [message, setMessage] = useState<string>("ㅤ");
  const [fileInfos, setFileInfos] = useState<Array<IFile>>([]);
  const [fileId, setFileId] = useState<string | null>(null)
  const [task_id, setTask] = useState(null);
  const [isLoad, setLoad] = useState(false);
  const [disc, setDisc] = useState<boolean>(false)
  const [status, setStatus] = useState<string>("ㅤ");
  const { lastMessage, sendMessage, readyState } = useWebSocket(`ws://localhost:8000/recognition/task/${task_id}/status`);
  const [ai, SetAi] = useState<string>("chatgpt");
  const [mod, SetMod] = useState<string>("text only");
  const selectFile = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { files } = event.target;
    const selectedFiles = files as FileList;
    setCurrentFile(selectedFiles?.[0]);
  };
  useEffect(() => {
    
    if (lastMessage){
      if (JSON.parse(lastMessage?.data).status != "COMPLETE"){
        if (currentFile){
          setCurrentFile1(currentFile);
        }
        
        setCurrentFile(undefined);
        setLoad(true);
        props.setLoad(true);
        setStatus(JSON.parse(lastMessage?.data).status);
      }else{
        setCurrentFile(currentFile1);
        console.log(lastMessage);
        console.log(JSON.parse(lastMessage.data));
        console.log(JSON.parse(lastMessage.data).result);
        const list = JSON.parse(lastMessage.data).result.responses;
        console.log(list);
        props.SetIdeas_s(list.recommendations);
        props.SetStructure_s(list.structure);
        props.SetSummary_s(list.summary);
        props.SetTags_s(list.tags);
        
        setStatus(JSON.parse(lastMessage?.data).status);
        props.setMessage(JSON.parse(lastMessage?.data).result);
        setLoad(false);
        props.setLoad(false);
      }
      
    }
    
  }, [lastMessage])

  const upload = () => {
    setProgress(0);
    if (!currentFile) return;

    UploadService.upload(currentFile, (event: any) => {
      setProgress(Math.round((100 * event.loaded) / event.total));
    })
      .then((response) => {
        setTask(response.data.task_id);
        http.post(`/recognition/task/${response.data.task_id}/start`, {
          analysis_mode: (mod == "text only" ? "text_only":"images"),
          model: ai,
          create_tags: props.tags,
          create_summary: props.summary,
          create_annotations: props.structure,
          create_ideas: props.ideas,
          prompt: props.prompt
        }, {
          headers: {
            "authorization": "Bearer " + Cookies.get('token')!,
          }},)
        
        sendMessage(JSON.stringify({
          "access_token": Cookies.get('token')//localStorage.getItem("token")!
          //access_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3NDUyMzI0MDN9.QbYdjCSYrEqLyhdiath0FrbWLsmCOBZpMf-HbeFvpxk"
      }))
        setFileId(response.fileid);
      })
      .catch((err) => {
        console.log(err);
        setStatus(err.response.data.detail);
        setProgress(0);
        if (err.response.data.detail == "Not authenticated"){
          router.replace('/#');
        }


      });
  };
  return (
    
        <Input id="picture" accept="image/jpeg,image/png" className="grid col-span-3" type="file" onChange={selectFile}/>     
   
  )
  
}