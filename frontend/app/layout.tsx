
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { ThemeProvider } from "@/components/theme-provider"
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { ModeToggle } from "@/components/theme-but";
import { HwProvider } from "@/components/globlalcont";
import ButT from "@/components/theme-but2";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable"
import "./globals.css";
import { createContext } from "vm";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  icons: {
        icon: '/favicon.ico', 
  },
  title: "CertSirius",
  description: "Made by ArtyRy",
};


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        suppressHydrationWarning
        className="allside "

      >
        <HwProvider>
          <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
            
                        
          >
            <SidebarProvider >
              <div className="allside ">
                <AppSidebar />
               
                  <div className="flex flex-row w-full pr-[15px] justify-end  mt-[10px] absolute">
                    <ButT/>
                  </div>
                  
                  {children}
               
                
             
              </div>
              
            </SidebarProvider>
          </ThemeProvider>
        </HwProvider>
        
      </body>
    </html>
  );
}
