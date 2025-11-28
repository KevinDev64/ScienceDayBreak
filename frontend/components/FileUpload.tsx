"use client"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useState, useContext } from "react";
import UploadService from "@/app/services/FileUploadService";
import IFile from "@/app/types/File";
import {Button} from "@/components/ui/button"
import "@/components/loading"
import { Progress } from "@/components/ui/progress"
import { useRouter } from 'next/navigation'



import http from "@/app/http-common"

type discard = {
  disc: boolean
  setDisc: React.Dispatch<React.SetStateAction<boolean>>
    
}


export function InputFile(props:any) {

  const router = useRouter()
  const [currentFile, setCurrentFile] = useState<File>();
  const [photo, setCurrentPhoto] = useState<File>();
  const [name, setName] = useState<string>("");
  const [descrip, setDiccription] = useState<string>("");
  const [date, setDate] = useState<string>("");
  const [progress, setProgress] = useState<number>(0);
  const selectFile = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { files } = event.target;
    const selectedFiles = files as FileList;
    setCurrentFile(selectedFiles?.[0]);
  };
  const selectPhoto = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { files } = event.target;
    const selectedFiles = files as FileList;
    setCurrentPhoto(selectedFiles?.[0]);
  };
  

  const upload = () => {
    setProgress(0);
    if (!currentFile || !photo) return;

    UploadService.upload(currentFile, photo, (event: any) => {
      setProgress(Math.round((100 * event.loaded) / event.total));
    })
      
  };
  return (
    <div className="flex flex-col">
        <div className="flex flex-row">
          <div>Название</div>
          <Input className="grid col-span-3" onChange={(e) => {setName(e.target.value)}} />
        </div>
        <div className="flex flex-row">
          <div>Дата</div>
          <Input className="grid col-span-3" onChange={(e) => {setDate(e.target.value)}} />
        </div>
        <div className="flex flex-row">
          <div>Описание</div>
          <Input className="grid col-span-3" onChange={(e) => {setDate(e.target.value)}} />
        </div>
        <Input id="picture" accept=".csv, text/csv"  className="grid col-span-3" type="file" onChange={selectFile}/>
        <Input id="pictur" accept="image/jpeg,image/png" className="grid col-span-3" type="file" onChange={selectPhoto}/>   
    </div>
          
   
  )
  
}