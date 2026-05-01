import { createContext, useState } from "react";
import { loginUser } from "../services/api";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  const login = async (data) => {
    const res = await loginUser(data);

    // backend return token/user check
    if (res.data?.token) {
      localStorage.setItem("token", res.data.token);
    }

    setUser(res.data.user || res.data);
    return res.data;
  };

  return (
    <AuthContext.Provider value={{ user, login }}>
      {children}
    </AuthContext.Provider>
  );
}