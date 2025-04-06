import React, { createContext, useContext, useState } from "react";

// Create context
const UserContext = createContext();

// Provider
export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    try {
      const stored = localStorage.getItem("user");
      return stored && stored !== "undefined" ? JSON.parse(stored) : null;
    } catch (err) {
      console.error("Failed to parse user from localStorage", err);
      return null;
    }
  });

  // Wrapper for updating context + localStorage
  const updateUser = (user) => {
    setUser(user);
    if (user) {
      localStorage.setItem("user", JSON.stringify(user));
    } else {
      localStorage.removeItem("user");
    }
  };

  return (
    <UserContext.Provider value={{ user, setUser: updateUser }}>
      {children}
    </UserContext.Provider>
  );
};

// Hook
export const useUser = () => useContext(UserContext);
