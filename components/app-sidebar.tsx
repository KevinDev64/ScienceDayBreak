"use client"


import { Ellipsis, Trash2 } from "lucide-react"
import { useRouter } from 'next/navigation'
import { useEffect, useState } from "react"
import Image from "next/image"
import { Check } from "lucide-react"
import Cookies from 'js-cookie'
import { ProgressD } from "./progressy"

import http from "@/app/http-common"
import { useHw } from "./globlalcont" 



import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
  SidebarSeparator,
  SidebarFooter,
  useSidebar,
} from "@/components/ui/sidebar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Skeleton } from "./ui/skeleton"





export function AppSidebar() {
  const site = useSidebar();

  const { historyTrigger } = useHw();
  const router = useRouter()

  const [isClient, setClient] = useState(false);
  const cont = useHw();
  
  const [prog3, setProg3] = useState(50);
  useEffect(() => {
    setClient(true)
  }, []);

  useEffect(() => {setProg3(cont.historyTrigger)}, [cont.historyTrigger])
  

  
  return (
    (isClient ? <Sidebar side="left">
      <SidebarSeparator />
      
      <SidebarContent className="z-30">
        <SidebarGroup>
          <SidebarGroupContent>
    {/*        
            <div className="flex flex-row items-center">
              <div className="mt-[4px] ml-[5px] p-1">
                {isClient ? <Image src="/l1.png" alt="Logo part 1" width={60} height={30} /> : <Skeleton className="h-[30px] w-[60px]" />}
              </div>
              <div className="mt-[4px] ml-[8px] p-1">
                {isClient ? <Image src="/l2.png" alt="Logo part 2" width={150} height={30} /> : <Skeleton className="h-[30px] w-[150px]" />}
              </div>
            </div>
            */}
          </SidebarGroupContent>
        </SidebarGroup>
        <div>

        </div>
        <div className="flex mt-[120px] flex-col items-center"> 
          <div className="w-[15px] h-[15px] rounded-[15px] bg-green-300">
            <Check className="ml-[1px] mt-[1px] text-background h-[13px] w-[13px]"/>
          </div>
          <ProgressD prog={100} />
          <div className="w-[15px] h-[15px] rounded-[15px] bg-green-300">
            <Check className="ml-[1px] mt-[1px] text-background h-[13px] w-[13px]"/>
          </div>
          <ProgressD prog={100}/>
          <div className="w-[15px] h-[15px] rounded-[15px] bg-green-300">
            <Check className="ml-[1px] mt-[1px] text-background h-[13px] w-[13px]"/>
          </div>
          <ProgressD prog={prog3}/>
          {prog3 < 100 ? <div className="w-[15px] h-[15px] rounded-[15px] bg-gray-500">

          </div> : 
              <div className="w-[15px] h-[15px] rounded-[15px] bg-green-300">
                <Check className="ml-[1px] mt-[1px] text-background h-[13px] w-[13px]"/>
              </div>
          }
          
        </div>
        

        
        {site.can && <SidebarRail />}
      </SidebarContent>

      
    </Sidebar>:<Skeleton/>)
  );
}