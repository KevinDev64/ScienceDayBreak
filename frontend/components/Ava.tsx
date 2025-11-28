"use client"
import {
    Avatar,
    AvatarFallback,
    AvatarImage,
  } from "@/components/ui/avatar"
import { useEffect } from "react"
import { useSidebar } from "./ui/sidebar"   
export function AvatarDemo(props:{size:string}) {
    const site=useSidebar()
    useEffect(()=>{
        site.setCan(true);
        site.setOpen(true)
    },[])
    return (
      <Avatar className={props.size}>
        <AvatarImage src="https://github.com/shadcn.png" alt="@shadcn" />
        <AvatarFallback>CN</AvatarFallback>
      </Avatar>
    )
  }