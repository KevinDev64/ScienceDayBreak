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
const homeworks = [
  {
    title: "Hw 1",
    url: "#",
    icon: ClipboardList,
  },
  {
    title: "Hw 2",
    url: "#",
    icon: ClipboardList,
  },
  {
    title: "Hw 3",
    url: "#",
    icon: ClipboardList,
  },
  {
    title: "Hw 4",
    url: "#",
    icon: ClipboardList,
  },
  {
    title: "Hw 5",
    url: "#",
    icon: ClipboardList,
  },
  {
    title: "Hw 6",
    url: "#",
    icon: ClipboardList,
  },
  {
    title: "Hw 7",
    url: "#",
    icon: ClipboardList,
  },
  {
    title: "Hw 8",
    url: "#",
    icon: ClipboardList,
  },
]
export function AppSidebar() {
  const site = useSidebar();
  const home = useHw();
  const [isClient, setClient] = useState(false);
  const [open, setOpen] = useState(false)
  const router = useRouter()
  useEffect(()=>{setClient(true)},[])
  return (

      <Sidebar side="left">
        <SidebarSeparator />
        
        <SidebarContent>
          <SidebarGroup>
            
          </SidebarGroup>
              
          <SidebarGroup>
            
            <SidebarGroupContent>
              <SidebarMenu>
              <SidebarMenuItem>
              <SidebarMenuButton asChild>
                <a href={"/event"}>
                    <Home />
                    <span>{"Create event"}</span>
                </a>
              </SidebarMenuButton>
                <SidebarMenuSub>
                  
                  
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
                              shadcn
                            </div>
                            <div>
                              shadcn@test.com
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
      </Sidebar>
 
    
  )
}