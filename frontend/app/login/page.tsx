"use client"


import {InputFile} from "@/components/FileUpload";
import { useState } from "react";
import { LoginForm } from "@/components/login-form"
import { useEffect } from "react";
import { Toaster, toast } from "sonner";
import {ModeToggle} from "@/components/theme-but"
import Cookies from 'js-cookie'
import http from "@/app/http-common";
import { useRouter } from 'next/navigation'
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
  SidebarSeparator,
  SidebarFooter,
  SidebarProvider,
  useSidebar
} from "@/components/ui/sidebar"
const login: React.FC = () => {
  const site = useSidebar();
  const router = useRouter();
  useEffect(() => {
    toast("Authorize please");
  },[])
  useEffect(() => {
    site.setCan(false);
    site.setOpen(false);
    if (Cookies.get('token') == null) return //localStorage.getItem("token")
    http.get("/auth/validation/", {
      headers: {
        "authorization": "Bearer " + Cookies.get('token')!//localStorage.getItem("token")!
        // "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3NDUyMzI0MDN9.QbYdjCSYrEqLyhdiath0FrbWLsmCOBZpMf-HbeFvpxk",
      },
    })
    .then(response => {
      if (response.data.status == "User exists!"){
        router.push('/hw-preview')
        site.setCan(true)
        setTimeout(() => {site.setOpen(true)}, 1000)
  
      }
    })
    .catch((err) => {
      router.replace('/#')
    });
  },[])
  return (
    <div className="flex flex-col grow-1">
      <div className="flex grow-1 w-full items-center justify-center p-6 md:p-10">
        <div className="w-full max-w-sm">
          <Toaster/>
          <LoginForm />
          
        </div>
    </div>
    </div>
    
  ) 
  
}
export default login;