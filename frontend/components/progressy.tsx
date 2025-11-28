"use client"

import * as React from "react"
import { Progress } from "@/components/ui/progress"

export function ProgressD({prog}:{prog:number}) {
  const [progress, setProgress] = React.useState(prog)
  const [displayProgress, setDisplayProgress] = React.useState(prog)

  React.useEffect(() => {
    setProgress(prog)
  }, [prog])


  React.useEffect(() => {
    const timer = setTimeout(() => {
      setDisplayProgress(progress)
    }, 10)
    return () => clearTimeout(timer)
  }, [progress])

  return (
    <div className="flex flex-col">
      <div 
        className="w-[2px] bg-green-300 transition-all duration-500 ease-in-out"
        style={{height: `${displayProgress * 1.5}px`}}
      >
      </div>
      <div 
        className="w-[2px] bg-gray-500 transition-all duration-500 ease-in-out"
        style={{height: `${(100 - displayProgress) * 1.5}px`}}
      >
      </div>
    </div>
  )
}