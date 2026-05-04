// frontend/src/pages/DocumentUpload.jsx

import { useState } from "react";
import axios from "axios";

export default function DocumentUpload() {

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {

    if (!file) {
      alert("Please select a file");
      return;
    }

    try {

      setLoading(true);

      const formData = new FormData();

      formData.append("file", file);

      console.log("Uploading file:", file);

      const res = await axios.post(
        "http://127.0.0.1:8000/documents/upload?task_id=1",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      console.log("UPLOAD RESPONSE:", res.data);

      alert("File uploaded successfully");

      setFile(null);

    } catch (err) {

      console.log("UPLOAD ERROR:", err);

      if (err.response) {
        console.log(err.response.data);
      }

      alert("Upload failed");

    } finally {

      setLoading(false);

    }
  };

  return (

    <div className="p-10 text-white">

      <h1 className="text-3xl font-bold mb-6">
        📂 Document Upload
      </h1>

      <div className="bg-white/10 p-6 rounded-2xl max-w-xl">

        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          className="mb-5 block"
        />

        <button
          onClick={handleUpload}
          disabled={loading}
          className="
            bg-blue-500
            hover:bg-blue-600
            px-6
            py-3
            rounded-xl
            font-bold
          "
        >
          {loading ? "Uploading..." : "Upload File"}
        </button>

      </div>

    </div>
  );
}