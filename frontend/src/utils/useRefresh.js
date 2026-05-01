import { useState } from "react";

export default function useRefresh() {
  const [refresh, setRefresh] = useState(false);

  const trigger = () => setRefresh((prev) => !prev);

  return [refresh, trigger];
}