"use client"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Upload } from "lucide-react"
import { useState } from "react"
import { InputFile } from "./FileUpload"
export function Dialogsol() {
    const [name, setName] = useState<string>("Shadcn");
    const [mail, setMail] = useState<string>("shadcn@test.com");
    return (
      <Dialog>
        <DialogTrigger asChild>
          <Button className="butsol" > <Upload/> </Button>
        </DialogTrigger>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Add solution</DialogTitle>
            <DialogDescription>
              Add your solution here. Click add when you're done.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="avatar" className="text-right">
                Solution
              </Label>
              <InputFile way="solve" className="grid col-span-3" />
            </div>
          </div>
          <DialogFooter>
            <Button type="submit">Add</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    )
  }