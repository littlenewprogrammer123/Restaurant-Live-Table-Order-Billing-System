import { createContext, useContext, useEffect, useState } from "react";
import api from "../api";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/auth/me/")
      .then(res => {
        setUser({ role: res.data.role.toUpperCase() });
      })
      .catch(() => {
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, []);

  const login = async (credentials) => {
    const res = await api.post("/login/", credentials);
    setUser({ role: res.data.role.toUpperCase() });
  };

  const logout = async () => {
    await api.post("/logout/");
    setUser(null);
  };

  if (loading) return <div>Loading...</div>;

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
