import Image from "next/image";
import { InputFile } from "@/components/FileUpload";
export default function Home() {
  return (
    <div className="main-container">
      <InputFile/>
    </div>
  );
}
