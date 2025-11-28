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
import { useState } from "react"
import { InputFile } from "./FileUpload"
export function Dialogus() {
    const [currentFile, setCurrentFile] = useState<File>();
    const selectFile = (event: React.ChangeEvent<HTMLInputElement>) => {
      const { files } = event.target;
      const selectedFiles = files as FileList;
      setCurrentFile(selectedFiles?.[0]);
    };
    const [name, setName] = useState<string>("Shadcn");
    const [mail, setMail] = useState<string>("shadcn@test.com");
    return (
      <Dialog>
        <DialogTrigger asChild>
          <Button variant="outline">Edit Profile</Button>
        </DialogTrigger>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Edit profile</DialogTitle>
            <DialogDescription>
              Make changes to your profile here. Click save when you're done.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="name" className="text-right">
                Name
              </Label>
              <Input id="name" value={name} onChange={(e) => {setName(e.target.value)}} className="col-span-3" />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="e-mail" className="text-right">
                E-mail
              </Label>
              <Input id="username" value={mail} onChange={(e) => {setMail(e.target.value)}} className="col-span-3" />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="avatar" className="text-right">
                Avatar
              </Label>
              <Input type="file" id="picture" accept="image/jpeg,image/png" onChange={selectFile} className="grid col-span-3" />
            </div>
          </div>
          <DialogFooter>
            <Button type="submit">Save changes</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    )
  }