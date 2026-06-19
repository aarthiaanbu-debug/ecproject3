import { useState } from "react";
import { uploadTaskDocument } from "../api/api";

export default function TaskDocuments() {
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    const formData = new FormData();

    formData.append("tenant_id", 1);
    formData.append("task_id", 1);
    formData.append("uploaded_by", 1);
    formData.append("file", file);

    await uploadTaskDocument(formData);

    alert("Uploaded Successfully");
  };

  return (
    <div className="p-6 text-white">
      <h1 className="text-3xl mb-5">
        Task Documents
      </h1>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button
        onClick={handleUpload}
        className="bg-green-600 px-4 py-2 rounded ml-4"
      >
        Upload
      </button>
    </div>
  );
}