"use client"

import * as React from "react"
import { useTheme } from "next-themes"
import Image from "next/image"
import { Skeleton } from "./ui/skeleton"

export function ModeToggle() {
  const { setTheme, theme } = useTheme()
  const [isClient, setClient] = React.useState(false)
  const [isMoving, setIsMoving] = React.useState(false)
  const [localTheme, setLocalTheme] = React.useState(theme)

  React.useEffect(() => { 
    setClient(true)
    setLocalTheme(theme)
  }, [theme])

  const toggleTheme = () => {
    setIsMoving(true)
    const newTheme = localTheme === "light" ? "dark" : "light"
    setLocalTheme(newTheme)
    
    // Ждем завершения анимации перед сменой темы
    setTimeout(() => {
      setTheme(newTheme)
      setIsMoving(false)
    }, 200) // Длительность анимации
  }

  return (
    isClient ? (
      <div 
        className="relative h-[25px] w-[50px] rounded-[15px] overflow-hidden cursor-pointer bg-gray-200 dark:bg-gray-700"
        onClick={toggleTheme}
      >
        {/* Фоновые изображения */}
        <div className={`absolute inset-0 transition-opacity duration-600 ease-in-out ${
          localTheme === "light" ? "opacity-100" : "opacity-0"
        }`}>
          <Image 
            src="/toogle_img.jpg"
            alt="Light background"
            fill
            className="object-cover"
            priority
          />
        </div>
        
        <div className={`absolute inset-0 transition-opacity duration-600 ease-in-out ${
          localTheme === "dark" ? "opacity-100" : "opacity-0"
        }`}>
          <Image 
            src="/night.jpg"
            alt="Dark background"
            fill
            className="object-cover"
            priority
          />
        </div>

        {/* Переключатель */}
        <div className={`
          absolute top-1/2 transform -translate-y-1/2 
          w-[17px] h-[17px] transition-all duration-300 ease-in-out
          ${localTheme === "light" ? "left-[5px]" : "left-[28px]"}
          ${isMoving ? "scale-110" : "scale-100"}
        `}>
          {/* Солнце */}
          <div className={`absolute inset-0 transition-all duration-900 ease-in-out ${
            localTheme === "light" ? "opacity-100" : "opacity-0"
          }`}>
            <Image 
              src="/sun.png"
              alt="Sun"
              width={17}
              height={17}
              className="object-cover rounded-[10px]"
              priority
            />
          </div>
          
          {/* Луна */}
          <div className={`absolute inset-0 transition-all duration-500 ease-in-out ${
            localTheme === "dark" ? "opacity-100" : "opacity-0"
          }`}>
            <Image 
              src="/moon.png"
              alt="Moon"
              width={17}
              height={17}
              className="object-cover rounded-[10px]"
              priority
            />
          </div>
        </div>
      </div>
    ) : (
      <Skeleton className="h-[25px] w-[50px] rounded-[15px]" />
    )
  )
}