
import { AvatarDemo } from "@/components/Ava"
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
import { Dialogus } from "@/components/profile-edit"
export default function LoginPage() {
  return (
    <div className="main-container">
      <AvatarDemo size="size-30" />
      <div className="flex grow-1 flex-col gap-10 items-center">
        <div className="flex flex-col items-start content-start gap-12 w-2xl">
          <div className="infarea">
            
            <div className="head">
              Name
            </div>
            <div className="bod">
              Shadcn
            </div>
          </div>
          <div className="infarea ">
            <div className="head">
              E-mail
            </div>
            <div className="bod">
              shadcn@test.com
            </div>
          </div>
        
          <div className="infarea">
            <div className="head">
              Rang
            </div>
            <div className="bod">
              Ultra
            </div>
          </div>
          <div className="infarea">
            <div className="head">
              Status
            </div>
            <div className="bod">
              Developer
            </div>
          </div>
        
        </div>
        <div>
          <Dialogus />
        </div>
        
      </div>
      
    </div>
  )
}