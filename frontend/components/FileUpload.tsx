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
import ButT from "./theme-but2";

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
    <div className="flex flex-col w-[45vw] gap-[2vh] justify-center">
        <div className="flex flex-row">
          <div className="w-[14vw]">Название</div>
          <Input className="grid col-span-3" onChange={(e) => {setName(e.target.value)}} />
        </div>
        <div className="flex flex-row">
          <div className="w-[14vw]">Дата</div>
          <Input className="grid col-span-3" onChange={(e) => {setDate(e.target.value)}} />
        </div>
        <div className="flex flex-row">
          <div className="w-[14vw]">Описание</div>
          <Input className="grid col-span-3" onChange={(e) => {setDate(e.target.value)}} />
        </div>
        <div className="flex flex-row">
          <div className="w-[14vw]">Участники</div>
          <Input id="picture" accept=".csv, text/csv"  className="grid col-span-3" type="file" onChange={selectFile}/>
        </div>
        <div className="flex flex-row">
          <div className="w-[14vw]">Шапка события</div>
          <Input id="pictur" accept="image/jpeg,image/png" className="grid col-span-3" type="file" onChange={selectPhoto}/>
        </div>
        <div className="flex flex-row items-center justify-center"> <Button className="w-[15vw]"> Отправить</Button></div>
        
        
    </div>
          
   
  )
  
}