"use client"
import { useState } from "react";
import Clouds from "./clouds";
import { Clouds2 } from "./clouds";
import { Moon, Star } from "./clouds";
import * as React from "react"
import { useTheme } from "next-themes"
import Image from "next/image"
import { Skeleton } from "./ui/skeleton"

export default function ButT(){
    const { setTheme, theme } = useTheme()
    const [isClient, setClient] = React.useState(false)
    const [isMoving, setIsMoving] = React.useState(false)
    const [localTheme, setLocalTheme] = React.useState(theme)
    const [theme1, setTheme1] = useState(theme)
    const toggleTheme = () => {
      
        const newTheme = theme1 === "light" ? "dark" : "light"
        setTheme1(newTheme)
        
        // Устанавливаем таймаут для завершения анимации перед переключением темы
        setTimeout(() => {
            setTheme(newTheme)
       
        }, 300) // Длительность соответствует CSS transition duration
    }
    React.useEffect(()=>{setClient(true)},[])
    const [night, setNight] = useState(false);
    React.useEffect(()=>{{theme != theme1 && 
        setTheme1(theme1 === "light" ? "dark" : "light")}},[theme])
    return(isClient ?
        (<div onClick={toggleTheme} className={`relative h-[25px] w-[50px] rounded-[15px] ${theme1 == "light" ? "bg-blue-400":"sky"} overflow-hidden transition-all duration-500 cursor-pointer`}>
            <div className="mt-[4px] relative">
                
                 <div className={ theme1 == "light" ? "absolute opacity-[0.9] mt-[12px] top-1/2 left-1/2 transition-all transform -translate-x-1/2 duration-500 -translate-y-1/2 scale-[0.2] z-10": "absolute opacity-[0] mt-[22px] top-1/2 left-1/2 transform transition-all duration-500  -translate-x-1/2 -translate-y-1/2 scale-[0.2] z-10"}> 
                    <Clouds /> 
                </div> 
               
                 <div className={ theme1 == "light" ? "absolute opacity-[0.5] mt-[10px] top-1/2 left-1/2 transform -translate-x-1/2 transition-all duration-500 -translate-y-1/2 scale-[0.2] z-10": "absolute opacity-[0] mt-[20px] top-1/2 left-1/2 transform -translate-x-1/2 transition-all duration-500 -translate-y-1/2 scale-[0.2] z-10"}>
                     <Clouds2/> 
                </div> 
                <div className={ theme1 == "light" ? "absolute mr-[10px] mb-[160px] h-[130px]  opacity-0 top-1/2 left-1/2 transition-all transform -translate-x-1/2 duration-400 w-[200px]  -translate-y-1/2 scale-[0.2] z-10": "absolute  mt-[12px] h-[130px] mr-[10px] top-1/2 left-1/2 transform transition-all duration-400 w-[200px]  -translate-x-1/2 -translate-y-1/2 scale-[0.2] z-10"}>
                    <div className="absolute scale-[0.2] ml-[40px]  mt-[40px]"><Star /> </div>
                    <div className="absolute scale-[0.3] ml-[60px] mt-[60px]  "><Star /> </div>
                    <div className="absolute scale-[0.3] "><Star /> </div>
                    <div className="absolute scale-[0.1] mt-[15px] ml-[30px] "><Star /> </div>
                    {/* <div className="absolute scale-[0.31] ml-[60px] mt-[5px]  "><Star /> </div> */}
                    <div className="absolute scale-[0.4] mt-[50px] "><Star /> </div>
                </div>
            
                <div className={theme1 == "light" ? "sun absolute z-20 ml-[5px] transition-all duration-500 pb-[4px] " : "sun absolute z-20 ml-[28px] transition-all duration-500 pb-[4px]"}>
              
                        <div className={theme1 == "light" ? "absolute z-30 opacity-0 top-1/2 left-1/2 transform -translate-x-1/2 transition-all duration-400 -translate-y-1/2 scale-[0.13]" : "absolute z-30  top-1/2 left-1/2 transform -translate-x-1/2 transition-all duration-400 -translate-y-1/2 scale-[0.13]"}>
                            <Moon className=" moon " />
                        </div>
                        

                </div>
            </div>
        </div>
    ):<Skeleton/>)
}