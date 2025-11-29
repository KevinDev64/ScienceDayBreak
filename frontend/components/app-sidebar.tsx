"use client"
import { Calendar, Home, Inbox, Search, Settings, ClipboardList } from "lucide-react"
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
  useSidebar,
  SidebarMenuSub,
  SidebarMenuSubItem,
  SidebarMenuSubButton,
} from "@/components/ui/sidebar"
import Cookies from 'js-cookie'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuPortal,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
  
} from "@/components/ui/dropdown-menu"
import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "@/components/ui/avatar"
import {AvatarDemo} from "@/components/Ava"
import http from "@/app/http-common"
import { useContext, useEffect, useState} from "react"
import Image from "next/image"
import { handleClientScriptLoad } from "next/script"
import { Label } from "@radix-ui/react-dropdown-menu"
import { useHw } from "./globlalcont"
import { Skeleton } from "./ui/skeleton"
// Menu items.
const items = [
  {
    title: "Homeworks",
    url: "#",
    icon: ClipboardList,
  },
]

export function AppSidebar() {
  const site = useSidebar();
  const home = useHw();
  const [isClient, setClient] = useState(false);
  const [open, setOpen] = useState(false)
  const [role, setRole] = useState('admin');
  const router = useRouter()
  const [exlist, setExlist] = useState([{name: "Digital marketing workshop", id: 0},{name: "Course state", id: 1},{name: "Math olimpiad", id: 2},{name: "Cybersecurity ctf", id: 3},]);
  useEffect(()=>{setClient(true)},[])
  useEffect(()=>{
      http.get("/user/events", {
        headers: {
          "authorization": "Bearer " + Cookies.get('token')!//localStorage.getItem("token")!
          // "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3NDUyMzI0MDN9.QbYdjCSYrEqLyhdiath0FrbWLsmCOBZpMf-HbeFvpxk",
        },
      })
      .then(response => {
        if (response.data.size > 0){
          setExlist(response.data);
        console.log(response.data);
        }
        
      })
      // .catch((err) => {
      //   router.replace('/login')
      // });
      if (Cookies.get('role')){
        
        console.log(typeof(Cookies.get('role')))
        console.log(role)
      }
      
      console.log("Cookies",Cookies.get('role'));
      console.log(role == 'admin')
  },[])
  return (

      (isClient && <Sidebar side="left">
        <SidebarSeparator />
        
        <SidebarContent>
          <SidebarGroup>
            
          </SidebarGroup>
              
          <SidebarGroup>
            
            <SidebarGroupContent>
              <SidebarMenu>
              <SidebarMenuItem>
              <SidebarMenuButton asChild>
                {Cookies.get('role') == 'admin' && <a href={"/event"}>
                    <Home />
                    <span>{"Create event"}</span>
                </a>}
                
                
              </SidebarMenuButton>
                <SidebarMenuSub>
                  
                  {exlist.map((ex:any, index) => (
                    <SidebarMenuSubItem key={index}>
                      <SidebarMenuSubButton className="hover:cursor-pointer" asChild>
                        <a  onClick={()=>{
                          
                        
                          router.replace("/ev?id=" + ex.id.toString())
                          window.location.reload()
    
                          
                          }}>
                          
                          <ClipboardList/>
                          <span >{ex.name}</span>
                        </a>
                      </SidebarMenuSubButton>
                    </SidebarMenuSubItem>
                  ))}
                </SidebarMenuSub>
              </SidebarMenuItem>
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
          {site.can && <SidebarRail />}
        </SidebarContent>
        <SidebarFooter>
            <SidebarMenu>
              <SidebarMenuItem>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    
                    <SidebarMenuButton style={{height:"70px"}}>
                      <div className="flex flex-row items-center justify-between grow-1">
                        <div className="flex flex-row gap-2 items-center">
                          <AvatarDemo size="size-10"/>
                          <div>
                            <div className="header">
                              {Cookies.get("usname") == undefined ? "shadcn" : Cookies.get("usname")}
                            </div>
                            <div>
                              {Cookies.get("email") == undefined ? "ex@mail.ru" : Cookies.get("email")}
                            </div>
                          </div>
                        </div>
                        
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-chevrons-up-down ml-auto size-4"><path d="m7 15 5 5 5-5"></path><path d="m7 9 5-5 5 5"></path></svg>
                      </div>
                        
                      
                    </SidebarMenuButton>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent
                    side="right"

                  >
                    <DropdownMenuItem onClick={() => {router.push("/accaunt")}}>
                      <span className="flex flex-row items-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-badge-check"><path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"></path><path d="m9 12 2 2 4-4"></path></svg>
                        <div>
                          Account
                        </div>
                        
                      </span>
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => {
                        Cookies.remove('token')
                        router.replace("/login")
                      }}>
                      <span className="flex flex-row items-center gap-2">
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-log-out"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" x2="9" y1="12" y2="12"></line></svg>
                        <div>
                          Log out
                        </div>
                        
                      </span>
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarFooter>
      </Sidebar>)
 
    
  )
}