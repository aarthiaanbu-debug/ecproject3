import { useState } from "react";
import { createWorkspace } from "../services/api";

export default function Workspace() {
  const [form, setForm] = useState({
    tenant_id: 1,
    name: "",
    slug: "",
    description: "",
    avatar_url: "",
    visibility: "PRIVATE",
    created_by: 1,
  });

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await createWorkspace(form);
      alert("Workspace Created Successfully");
    } catch (err) {
      console.log(err);
      alert("Failed");
    }
  };

  return (
    <div className="p-6 text-white">
      <h1 className="text-2xl font-bold mb-4">Workspace Management</h1>

      <form onSubmit={handleSubmit} className="space-y-3">
        <input
          className="w-full p-2 text-black"
          placeholder="Workspace Name"
          onChange={(e) =>
            setForm({ ...form, name: e.target.value })
          }
        />

        <input
          className="w-full p-2 text-black"
          placeholder="Slug"
          onChange={(e) =>
            setForm({ ...form, slug: e.target.value })
          }
        />

        <textarea
          className="w-full p-2 text-black"
          placeholder="Description"
          onChange={(e) =>
            setForm({ ...form, description: e.target.value })
          }
        />

        <select
          className="w-full p-2 text-black"
          onChange={(e) =>
            setForm({ ...form, visibility: e.target.value })
          }
        >
          <option value="PRIVATE">PRIVATE</option>
          <option value="PUBLIC">PUBLIC</option>
        </select>

        <button
          className="bg-blue-600 px-4 py-2 rounded"
          type="submit"
        >
          Create Workspace
        </button>
      </form>
    </div>
  );
}