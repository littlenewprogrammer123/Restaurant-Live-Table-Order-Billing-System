import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import api from "../api";
import { useAuth } from "../context/AuthContext";

function Manager() {
  const { user } = useAuth();

  // -------------------------
  // STATE
  // -------------------------
  const [tables, setTables] = useState([]);
  const [menu, setMenu] = useState([]);

  const [newTableNumber, setNewTableNumber] = useState("");
  const [newMenuName, setNewMenuName] = useState("");
  const [newMenuPrice, setNewMenuPrice] = useState("");

  const [loading, setLoading] = useState(true);

  // -------------------------
  // LOAD DATA
  // -------------------------
  const loadAll = async () => {
    try {
      const [tablesRes, menuRes] = await Promise.all([
        api.get("/tables/"),
        api.get("/menu/"),
      ]);

      setTables(Array.isArray(tablesRes.data) ? tablesRes.data : []);
      setMenu(Array.isArray(menuRes.data) ? menuRes.data : []);
    } catch (err) {
      console.error(err);
      alert("Failed to load manager data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAll();
  }, []);

  // -------------------------
  // TABLE ACTIONS
  // -------------------------
  const addTable = async () => {
    if (!newTableNumber) {
      return alert("Table number required");
    }

    try {
      await api.post("/tables/create/", {
        number: Number(newTableNumber),
      });

      setNewTableNumber("");
      loadAll();
    } catch (err) {
      alert(
        err.response?.data?.number?.[0] ||
          "Failed to add table (duplicate?)"
      );
    }
  };

  const updateTableStatus = async (tableId, isAvailable) => {
    try {
      await api.post(`/tables/${tableId}/status/`, {
        is_available: isAvailable,
      });
      loadAll();
    } catch {
      alert("Failed to update table status");
    }
  };

  // -------------------------
  // MENU ACTIONS
  // -------------------------
  const addMenuItem = async () => {
    if (!newMenuName || !newMenuPrice) {
      return alert("Name and price required");
    }

    try {
      await api.post("/menu/create/", {
        name: newMenuName,
        price: Number(newMenuPrice),
        is_active: true,
      });

      setNewMenuName("");
      setNewMenuPrice("");
      loadAll();
    } catch {
      alert("Failed to add menu item");
    }
  };

  const toggleMenuItem = async (itemId) => {
    try {
      await api.post(`/menu/${itemId}/toggle/`);
      loadAll();
    } catch {
      alert("Failed to update menu item");
    }
  };

  // -------------------------
  // ACCESS CONTROL
  // -------------------------
  if (!user || user.role !== "MANAGER") {
    return <div className="p-3">Access denied</div>;
  }

  if (loading) {
    return <div className="p-3">Loading manager dashboard...</div>;
  }

  return (
    <Layout>
      <h4 className="mb-3">Manager Dashboard</h4>

      {/* ========================= */}
      {/* MENU MANAGEMENT */}
      {/* ========================= */}
      <div className="card p-3 mb-4">
        <h6>Menu Management</h6>

        <div className="row g-2 mb-3">
          <div className="col">
            <input
              className="form-control"
              placeholder="Item name"
              value={newMenuName}
              onChange={(e) => setNewMenuName(e.target.value)}
            />
          </div>
          <div className="col">
            <input
              type="number"
              className="form-control"
              placeholder="Price"
              value={newMenuPrice}
              onChange={(e) => setNewMenuPrice(e.target.value)}
            />
          </div>
          <div className="col-auto">
            <button className="btn btn-success" onClick={addMenuItem}>
              Add Item
            </button>
          </div>
        </div>

        <table className="table table-sm table-bordered">
          <thead>
            <tr>
              <th>Name</th>
              <th>Price</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {menu.map((m) => (
              <tr key={m.id}>
                <td>{m.name}</td>
                <td>₹{m.price}</td>
                <td>{m.is_active ? "ACTIVE" : "DISABLED"}</td>
                <td>
                  <button
                    className={`btn btn-sm ${
                      m.is_active
                        ? "btn-outline-danger"
                        : "btn-outline-success"
                    }`}
                    onClick={() => toggleMenuItem(m.id)}
                  >
                    {m.is_active ? "Disable" : "Enable"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* ========================= */}
      {/* TABLE MANAGEMENT */}
      {/* ========================= */}
      <div className="card p-3 mb-4">
        <h6>Add New Table</h6>
        <div className="d-flex gap-2">
          <input
            type="number"
            className="form-control"
            value={newTableNumber}
            onChange={(e) => setNewTableNumber(e.target.value)}
          />
          <button className="btn btn-success" onClick={addTable}>
            Add
          </button>
        </div>
      </div>

      <h6>Tables</h6>
      <table className="table table-bordered align-middle">
        <thead>
          <tr>
            <th>Table</th>
            <th>Availability</th>
            <th>Change</th>
          </tr>
        </thead>
        <tbody>
          {tables.map((table) => (
            <tr key={table.id}>
              <td>Table {table.number}</td>
              <td>{table.is_available ? "AVAILABLE" : "OCCUPIED"}</td>
              <td>
                <select
                  className="form-select"
                  value={table.is_available ? "YES" : "NO"}
                  onChange={(e) =>
                    updateTableStatus(
                      table.id,
                      e.target.value === "YES"
                    )
                  }
                >
                  <option value="YES">AVAILABLE</option>
                  <option value="NO">OCCUPIED</option>
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </Layout>
  );
}

export default Manager;
