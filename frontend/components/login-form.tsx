"use client"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import gif from './assets/animation.gif';
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import http from '@/app/http-common'
import React, { useState } from 'react';
import { useRouter } from 'next/navigation'
import { Toaster, toast } from "sonner";
import Cookies from 'js-cookie'
import { Eye } from "lucide-react";
import { EyeClosed } from "lucide-react";
import {
  useSidebar
} from "@/components/ui/sidebar"

export function LoginForm({
  className,
  ...props
}: React.ComponentPropsWithoutRef<"div">) {
  const vivod = (email_log: string, password_log: string) =>{
    console.log(email_log, password_log)
  }
  const site = useSidebar();
  const router = useRouter()
  const [response, setResponse] = useState({});
  const [email_log, setEmail_log] = useState("");
  const [password_log, setPassword_log] = useState("");
  const [visible, setVisible] = useState("password");
  function VisBut(){
    return <Button className="nonebutvis"  onClick={() => {setVisible(visible == "password" ? "":"password")}}> {visible == "password" ?<Eye />:<EyeClosed/>} </Button>;
  }
  const login = (e: any) => {
    e.preventDefault()
    http.post("/auth/login", {email: email_log, password: password_log})
        .then(response => {
          if (response.data){
            console.log(response.data.id)
            toast("successful login")
            router.push("/hw-preview")
            site.setCan(true)
            setTimeout(() => {site.setOpen(true)}, 1000)
            //localStorage.setItem('token', response.data.access_token)<img src={"@/public/0017"} alt="loading..." />
            Cookies.set('token', response.data.access_token, { expires: 7 })
          }
        })
        .catch((err) => {
          console.log(err);
          if (err.response.data.detail == "User not correct password"){
            toast("incorrect an email or a password")
            router.replace('/#');
          }
        });
  }
  return (
    <div>
      
      <div className={cn("flex flex-col", className)} {...props}>
        <Card>
          {password_log != "" && <div id={"nonebutvis"} className="nonebutvis"> <VisBut /> </div>}
          <CardHeader>
            <CardTitle className="text-2xl">Login</CardTitle>
            <CardDescription>
              Enter your email below to login to your account
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form>
              <div className="flex flex-col gap-6">
                <div className="grid gap-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="m@example.com"
                    required
                    onChange={(e) => setEmail_log(e.target.value)}
                    
                  />
                </div>
                <div className="grid gap-2">
                  <div className="flex items-center">
                    <Label htmlFor="password">Password</Label>
                    <a
                      href="#"
                      className="ml-auto inline-block text-sm underline-offset-4 hover:underline"
                    >
                      Forgot your password?
                    </a>
                  </div>
                  <Input 
                    id="password" 
                    type={visible}
                    required 
                    onChange={(e) => setPassword_log(e.target.value)}
                  />
                  
                </div>
                
                <Button type="submit" className="w-full  cursor-pointer" onClick={login}>
                  Login
                </Button>
                
              </div>
              
              <div className="mt-4 text-center text-sm">
                Don&apos;t have an account?{" "}
                <a href="/" className="underline underline-offset-4">
                  Sign up
                </a>
              </div>
            </form>
            
          </CardContent>
        </Card>
        <Toaster />
      </div>
    </div>
    
  )
}