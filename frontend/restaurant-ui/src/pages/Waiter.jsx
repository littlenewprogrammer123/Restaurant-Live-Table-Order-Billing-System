import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import api from "../api";
import { useAuth } from "../context/AuthContext";

function Waiter() {
  const { user } = useAuth();

  const [tables, setTables] = useState([]);
  const [menu, setMenu] = useState([]);

  const [activeTable, setActiveTable] = useState(null);
  const [order, setOrder] = useState(null);
  const [orderItems, setOrderItems] = useState([]);

  const [loading, setLoading] = useState(true);

  // -------------------------
  // LOAD TABLES + MENU
  // -------------------------
  const loadInitialData = async () => {
    try {
      const [tablesRes, menuRes] = await Promise.all([
        api.get("/tables/"),
        api.get("/menu/"),
      ]);
      setTables(tablesRes.data);
      setMenu(menuRes.data);
    } catch (err) {
      console.error("Failed to load waiter data", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user?.role === "WAITER") {
      loadInitialData();
    }
  }, [user]);

  // -------------------------
  // CREATE NEW ORDER
  // -------------------------
  const startOrder = async (table) => {
    try {
      const res = await api.post("/orders/create/", {
        table_id: table.id,
      });

      setActiveTable(table);
      setOrder(res.data);
      setOrderItems([]);
    } catch {
      alert("Failed to create order");
    }
  };

  // -------------------------
  // OPEN EXISTING ORDER
  // -------------------------
  const openOrder = async (table) => {
    try {
      const res = await api.get(`/orders/table/${table.id}/`);
      if (!res.data || res.data.length === 0) {
        alert("No active order found");
        return;
      }

      setActiveTable(table);
      setOrder(res.data[0]);
      setOrderItems(res.data[0].items);
    } catch {
      alert("Failed to load order");
    }
  };

  // -------------------------
  // REFRESH ORDER
  // -------------------------
  const refreshOrder = async () => {
    if (!activeTable) return;
    const res = await api.get(`/orders/table/${activeTable.id}/`);
    setOrder(res.data[0]);
    setOrderItems(res.data[0].items);
  };

  // -------------------------
  // ADD ITEM (MERGED BACKEND)
  // -------------------------
  const addItem = async (menuItem) => {
    if (!order || order.status !== "OPEN") return;

    await api.post(`/orders/${order.id}/items/`, {
      menu_item_id: menuItem.id,
      quantity: 1,
    });

    refreshOrder();
  };

  // -------------------------
  // UPDATE QTY (DELETE IF < 1)
  // -------------------------
  const updateQty = async (itemId, qty) => {
    if (!order || order.status !== "OPEN") return;

    await api.patch(`/orders/items/${itemId}/`, {
      quantity: qty,
    });

    refreshOrder();
  };

  // -------------------------
  // REQUEST BILL (FINAL STEP)
  // -------------------------
  const requestBill = async () => {
    if (!order) return;

    try {
      await api.post(`/orders/${order.id}/request-bill/`);

      // 🔥 RESET EVERYTHING CLEANLY
      setActiveTable(null);
      setOrder(null);
      setOrderItems([]);

      // reload tables to reflect availability
      loadInitialData();
    } catch {
      alert("Failed to request bill");
    }
  };

  // -------------------------
  // GUARDS
  // -------------------------
  if (!user || user.role !== "WAITER") {
    return <div>Access denied</div>;
  }

  if (loading) {
    return <div>Loading...</div>;
  }

  const isEditable = order?.status === "OPEN";

  return (
    <Layout>
      <h4>Waiter Dashboard</h4>

      {/* TABLE SELECTION */}
      {!activeTable && (
        <>
          <h6>Select Table</h6>
          <div className="d-flex gap-2 flex-wrap">
            {tables.map((t) => (
              <button
                key={t.id}
                className={`btn ${
                  t.status === "AVAILABLE"
                    ? "btn-outline-success"
                    : t.status === "OCCUPIED"
                    ? "btn-outline-primary"
                    : "btn-outline-secondary"
                }`}
                disabled={t.status === "BILL_REQUESTED"}
                onClick={() => {
                  if (t.status === "AVAILABLE") {
                    startOrder(t);
                  } else if (t.status === "OCCUPIED") {
                    openOrder(t);
                  }
                }}
              >
                Table {t.number} – {t.status}
              </button>
            ))}

          </div>
        </>
      )}

      {/* ORDER PANEL */}
      {activeTable && (
        <div className="row mt-4">
          {/* MENU */}
          <div className="col-md-6">
            <h6>Menu</h6>

            {menu.map((m) => (
              <div
                key={m.id}
                className="d-flex justify-content-between border p-2 mb-2"
              >
                <span>
                  {m.name} – ₹{m.price}
                </span>
                <button
                  className="btn btn-sm btn-success"
                  disabled={!isEditable}
                  onClick={() => addItem(m)}
                >
                  Add
                </button>
              </div>
            ))}
          </div>

          {/* ORDER ITEMS */}
          <div className="col-md-6">
            <h6>Order – Table {activeTable.number}</h6>

            {orderItems.length === 0 && (
              <p className="text-muted">No items added yet</p>
            )}

            {orderItems.map((item) => (
              <div
                key={item.id}
                className="d-flex justify-content-between align-items-center border p-2 mb-2"
              >
                <span>{item.menu_item.name}</span>
                <div className="d-flex gap-2 align-items-center">
                  <button
                    className="btn btn-sm btn-outline-secondary"
                    disabled={!isEditable}
                    onClick={() =>
                      updateQty(item.id, item.quantity - 1)
                    }
                  >
                    −
                  </button>
                  <strong>{item.quantity}</strong>
                  <button
                    className="btn btn-sm btn-outline-secondary"
                    disabled={!isEditable}
                    onClick={() =>
                      updateQty(item.id, item.quantity + 1)
                    }
                  >
                    +
                  </button>
                </div>
              </div>
            ))}

            {/* REQUEST BILL */}
            <button
              className="btn btn-warning w-100 mt-3"
              disabled={!isEditable || orderItems.length === 0}
              onClick={requestBill}
            >
              Request Bill
            </button>

            {!isEditable && (
              <small className="text-muted">
                Order is locked after bill request
              </small>
            )}
          </div>
        </div>
      )}
    </Layout>
  );
}

export default Waiter;
