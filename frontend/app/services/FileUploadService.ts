import http from "../http-common";
import Cookies from 'js-cookie'
const upload = (file: File, photo : File,  name: string, date: string, descr: string, onUploadProgress: any): Promise<any> => {
  const formData = new FormData();
  formData.append("name", name);
  formData.append("date_str", date);
  formData.append("description", descr);
  formData.append("image", photo);
  formData.append("csv_file", file);
  console.log(file, photo)
  return http.post("/operator/event", formData, {
    headers: {
      "authorization": "Bearer " + Cookies.get('token')!,
    }
  });
};


const FileUploadService = {
  upload,
};


export default FileUploadService;