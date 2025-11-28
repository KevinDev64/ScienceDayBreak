"use client"
import {
  ContextMenu,
  ContextMenuCheckboxItem,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuLabel,
  ContextMenuRadioGroup,
  ContextMenuRadioItem,
  ContextMenuSeparator,
  ContextMenuShortcut,
  ContextMenuSub,
  ContextMenuSubContent,
  ContextMenuSubTrigger,
  ContextMenuTrigger,
} from "@/components/ui/context-menu"

import { Trash2 } from "lucide-react"
import { PencilLine } from "lucide-react"
import { useState } from "react"
import Cookies from 'js-cookie'
import { useContext } from "react"

export function ContextMenusol(
    {
        children,
        ...props
    }: React.ComponentProps<"div">
) {
  const [open, setOpen] = useState(false)
  
  return (

    <ContextMenu>
      <ContextMenuTrigger className="flex  items-center justify-center rounded-md w-auto  text-sm">
        {children}
      </ContextMenuTrigger>
      <ContextMenuContent >
        <ContextMenuItem  inset asChild>
         
        </ContextMenuItem>
        
      </ContextMenuContent>
    </ContextMenu>
  )
}
