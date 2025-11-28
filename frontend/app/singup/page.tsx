"use client"
import "../globals.css";

import {InputFile} from "@/components/FileUpload";
import { useState } from "react";
import { SingupForm } from "@/components/singup-form"
import {ModeToggle} from "@/components/theme-but"

const login: React.FC = () => {
  return (
    <div  className="flex flex-col grow-1" >
    <div className="flex grow-1 w-full items-center justify-center p-6 md:p-10">
      <div className="w-full max-w-sm">
        <SingupForm />
      </div>
    </div>
    </div>
    
  ) 
  
}
export default login;