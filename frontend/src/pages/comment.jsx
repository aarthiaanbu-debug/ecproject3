import { useEffect, useState } from "react";
import { getComments, createComment } from "../services/api";

export default function Comments({ taskId }) {
  const [comments, setComments] = useState([]);

  const load = async () => {
    const res = await getComments(taskId);
    setComments(res.data);
  };

  useEffect(() => {
    load();
  }, []);

  const addComment = async () => {
    await createComment({
      task_id: taskId,
      content: "Nice work"
    });
    load();
  };

  return (
    <div>
      <h3>Comments</h3>

      <button onClick={addComment}>Add</button>

      {comments.map(c => (
        <p key={c.id}>{c.content}</p>
      ))}
    </div>
  );
}