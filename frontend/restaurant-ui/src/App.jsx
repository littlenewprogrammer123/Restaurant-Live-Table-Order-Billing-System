import { useAuth } from "./context/AuthContext";
import Login from "./pages/Login";
import Tables from "./pages/Tables";
import Waiter from "./pages/Waiter";
import Cashier from "./pages/Cashier";
import Manager from "./pages/Manager";

function App() {
  const { user } = useAuth();

  if (!user) {
    return <Login />;
  }

  return (
    <>
      {user.role === "WAITER" && <Waiter />}
      {user.role === "CASHIER" && <Cashier />}
      {user.role === "MANAGER" && <Manager />}

      {/* Tables visible to all logged-in users */}
      <Tables />
    </>
  );
}

export default App;
