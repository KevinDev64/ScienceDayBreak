import http from "../http-common";
import Cookies from 'js-cookie'
const upload = (file: File, onUploadProgress: any): Promise<any> => {
  const formData = new FormData();

  formData.append("file", file);

  return http.post("/recognition/task", formData, {
    headers: {
      "authorization": "Bearer " + Cookies.get('token')!,
    },
    onUploadProgress,
  });
};


const FileUploadService = {
  upload,
};


export default FileUploadService;